# -*- coding: utf-8 -*-

"""
Default ResponseView classes for ipyrest.
"""

import re
import io
import json
from math import log, fabs
from collections import OrderedDict
from typing import Dict, Tuple, List, Union, Optional, Any, Callable

import geojson
import requests
import ipyvolume
import ipyleaflet
import pandas as pd
from ipywidgets import (Widget, HBox, VBox, Text, Textarea,
                        Button, Layout, Tab, Image, HTML)
from qgrid import QGridWidget


# Bounding box functions related to GeoJSONResponseView

def geojson_bbox(gj_object) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    Return bbox for a GeoJSON object as ((min_lon, min_lat), (max_lon, max_lat)).
    """
    gj = geojson.loads(json.dumps(gj_object))
    coords = []
    for feat in gj['features']:
        coords += list(geojson.coords(feat))
    coords = tuple(coords)
    bbox = min(coords), max(coords)
    return bbox


def bbox_center(p: Tuple[float, float],
                q: Tuple[float, float]) -> Tuple[float, float]:
    """
    Return middle point between two points p and q.
    """
    (min_lon, min_lat), (max_lon, max_lat) = p, q
    center = min_lon + (max_lon - min_lon) / 2, min_lat + \
        (max_lat - min_lat) / 2
    return center


def zoom_for_bbox(lon_min: float,
                  lat_min: float,
                  lon_max: float,
                  lat_max: float) -> int:
    """
    Return zoom level for some bounding box.
    """
    lat_diff = fabs(lat_max - lat_min)
    lon_diff = fabs(lon_max - lon_min)
    max_diff = max(lon_diff, lat_diff)

    if max_diff < 360 / 2**20:
        zoom_level = 21
    else:
        zoom_level = int(-1 * ((log(max_diff) / log(2)) - (log(360) / log(2))))
        if zoom_level < 1:
            zoom_level = 1
    return zoom_level


# All response views render a requests.Response object as an ipywidget.

class ResponseView(object):
    """
    Abstract view baseclass for rendering a ``requests.Response`` object
    into an ipywidgets.Widget.
    """

    def __init__(self, owner=None) -> None:
        "Create a new ResponseView. The owner is the API using it."

        self.owner = owner
        self.data = None

    def render(self, resp: requests.models.Response) -> Optional[Widget]:
        "Return some rendered 'view' of the response or None."

        return None


class RawResponseView(object):
    """
    A view that renders a raw response in an ipywidgets.Textarea.
    """
    name = 'Raw'
    mimetype_pats = ['.*']

    def render(self, resp: requests.models.Response) -> Optional[Widget]:
        "Return some rendered raw 'view' of the response or None."

        obj = resp.content
        self.data = obj
        layout = Layout(width='100%', height='100%')
        ta = Textarea(layout=layout)
        try:
            ta.value = str(resp.content.decode(resp.encoding)) \
                if resp.encoding else str(resp.content)
        except UnicodeDecodeError:
            ta.value = str(resp.content)
        num_lines = ta.value.count('\n')
        ta.rows = min(10, num_lines + 1)
        return ta


class HTMLResponseView(ResponseView):
    """
    A view that renders HTML in an ipywidgets.HTML.
    """
    name = 'HTML'
    mimetype_pats = ['text/html.*']

    def render(self, resp: requests.models.Response) -> HTML:
        "Return HTML rendered using an HTML ipywidget, or None."

        obj = resp.content
        try:
            self.data = obj.decode('utf-8')
            h = HTML(self.data)
        except:
            self.data = obj
            h = HTML(obj)
        return h


class SVGResponseView(ResponseView):
    """
    A view that renders SVG somehow.
    """
    name = 'SVG'
    mimetype_pats = ['image/svg\+xml.*']

    def render(self, resp: requests.models.Response) -> HTML:
        "Return SVG soehow, or None."

        obj = resp.content
        try:
            self.data = obj.decode('utf-8')
            h = HTML(self.data)
        except:
            self.data = obj
            h = HTML(obj)
        return h


class ImageResponseView(ResponseView):
    """
    A view that renders a bitmap image in an ipywidgets.Image.
    """
    name = 'Image'
    mimetype_pats = ['image/.*']

    def render(self, resp: requests.models.Response) -> Image:
        "Return an ipywidget image with the data object rendered on it, or None."

        obj = resp.content
        ct = resp.headers['Content-Type']
        maintype, subtype, params = re.match(
            '(\w+)/([\.\+\w]+)(;.*)?', ct).groups()
        img = Image(value=obj, format=subtype)
        self.data = img
        return img


class JSONResponseView(ResponseView):
    """
    A view that renders JSON in some semi-pretty form in an ipywidgets.Textarea.
    """
    name = 'JSON'
    mimetype_pats = ['application/json.*', 'application/vnd\..*\+json.*']

    def render(self, resp: requests.models.Response) -> Textarea:
        "Return a somewhat prettified JSON string."

        obj = resp.json()
        self.data = obj
        layout = Layout(width='100%', height='100%')
        ta = Textarea(layout=layout)
        value = json.dumps(obj, indent=2)
        ta.value = value
        num_lines = value.count('\n')
        ta.rows = min(10, num_lines + 1)
        return ta


class CSVResponseView(ResponseView):
    """
    A view that renders CSV data as an interactive table
    """
    name = 'CSV'
    mimetype_pats = ['text/csv.*']

    def render(self, resp: requests.models.Response) -> QGridWidget:
        "Return an interactive grid with the CSV data"

        csv = io.StringIO(resp.text)
        df = pd.read_csv(csv)
        self.data = df
        grid = QGridWidget(df=df)
        return grid


class GeoJSONResponseView(ResponseView):
    """
    A view that renders GeoJSON on an ipyleaflet.Map.
    """
    name = 'GeoJSON'
    mimetype_pats = ['application/vnd\.geo\+json.*']

    def render(self, resp: requests.models.Response) -> ipyleaflet.Map:
        "Return an ipyleaflet map with the GeoJSON object rendered on it, or None."

        obj = resp.json()
        if obj.get('type', None) != 'FeatureCollection':
            return None
        bbox = geojson_bbox(obj)
        mins, maxs = bbox
        center = list(reversed(bbox_center(*bbox)))
        z = zoom_for_bbox(*(mins + maxs))
        m = ipyleaflet.Map(center=center, zoom=z + 1)
        m.add_layer(layer=ipyleaflet.GeoJSON(data=obj))
        self.data = m
        return m


class GPXResponseView(ResponseView):
    """
    A view that renders GPS traces in GPX format on an ipyleaflet.Map.

    See https://www.topografix.com/gpx.asp
    """
    name = 'GPX'
    mimetype_pats = ['application/gpx\+xml.*']

    def render(self, resp: requests.models.Response) -> ipyleaflet.Map:
        "Return an ipyleaflet map with the GPX object rendered on it, or None."

        import gpxpy
        from gpxpy.gpx import GPXXMLSyntaxException

        obj = resp.content.decode('utf-8')
        try:
            trace = gpxpy.parse(obj)
        except GPXXMLSyntaxException:
            return None
        pts = [p.point for p in trace.get_points_data()]
        bbox = trace.get_bounds()
        mins = (bbox.min_latitude, bbox.min_longitude)
        maxs = (bbox.max_latitude, bbox.max_longitude)
        bbox = mins, maxs
        center = list(bbox_center(*bbox))
        z = zoom_for_bbox(*(mins + maxs))
        m = ipyleaflet.Map(center=center, zoom=z + 1)
        # FIXME: make path styling configurable
        poly = ipyleaflet.Polyline(locations=[(p.latitude, p.longitude)
            for p in pts], fill=False)
        m.add_layer(layer=poly)
        for p in pts:
            cm = ipyleaflet.CircleMarker(location=(p.latitude, p.longitude), radius=5)
            m.add_layer(layer=cm)
        self.data = m
        return m


class Scatter3DResponseView(ResponseView):
    """
    A view that renders 3D scatter plot data as dots in an ipyvolume widget.

    The data source is expected to be a table with three or more columns
    of which the first three are taken to by x, y, and z.
    """
    name = 'Scatter-3D'
    mimetype_pats = ['application/vnd\.3d\+txt.*']

    def render(self, resp: requests.models.Response) -> Widget:
        "Return an ipyvolume widget with the data object rendered on it."

        f = io.BytesIO(resp.content)
        points = pd.read_csv(f, delim_whitespace=True)
        # points = points[:: 300] # FIXME: use down-sampling here
        x = points.iloc[:, 0].values
        y = points.iloc[:, 1].values
        z = points.iloc[:, 2].values
        res = ipyvolume.quickscatter(x, y, z, size=1, marker="sphere")

        return res


class ProtobufResponseView(ResponseView):
    """
    A view that renders Protobuf objects deserialized into text.
    """
    name = 'Protobuf'
    mimetype_pats = ['application/x\-protobuf.*']

    def render(self, resp: requests.models.Response) -> Textarea:
        "Return deserialized Protobuf objects as text inside a Textarea."

        obj = resp.content
        import addressbook_pb2
        person = addressbook_pb2.Person()
        person.ParseFromString(obj)
        self.data = person
        layout = Layout(width='100%', height='100%')
        ta = Textarea(layout=layout)
        ta.value = str(person)
        return ta


# A list of all built-in ResponseView subclasses in this module:

builtin_view_classes = [
    n for (k, n) in globals().items()
    if type(n) == type and issubclass(n, ResponseView) and n != ResponseView]
