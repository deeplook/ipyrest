# Ipyrest

Ipyrest is an emerging Jupyter widget for exploring RESTful APIs still in alpha state. It has two main goals: provide a more intuitive interface in the spirit of Postman, and allow to plug-in components, starting with output renderers for various MIME types, e.g. GeoJSON:

![banner](banner.png "")

More to come...

Concepts:

- Server
- Service
- Request
- Response
- Data
- MIME-Type
- Compression (not explicitly, yet)
- Logging (not well enough, yet)
- Caching
- Time-Out
- Errors (our own, not yet)
- Viewing
- Plugins
- Testing
- UI

Response views (plugins):

- Text
- HTML
- Bitmaps
- SVG
- JSON
- GeoJSON
- Protobuf
- 3D ?

Main direct dependencies:

- Python >= 3.6
- jupyter (incl. lab)
- ipywidgets
- ipyleaflet
- ipyvolume
- geojson
- protobuf
- timeout_decorator
- requests
- vcr
- mypy
- pytest

Issues:

- Traitlets limitations (mainly on compound widgets)
- Text styling (ipywidgets.HTML)
- CesiumJS (not an ipywidget)
