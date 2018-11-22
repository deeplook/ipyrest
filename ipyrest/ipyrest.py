# -*- coding: utf-8 -*-

"""
This is a Postman-like IPyWidgets compound widget for exploring Rest APIs.
It aims at providing more flexible options for customization and adding
custom views to display e.g. GeoJSON and image responses directly in
the interface. These should at some point also include UI widgets like
sliders etc to make it easier to vary the input request.
"""

import os
import re
import json
import urllib
import logging
from math import log, fabs
from collections import OrderedDict
from urllib.parse import (parse_qs, parse_qsl, splitquery,
                          urlparse, urlunparse)

import vcr
import requests
import timeout_decorator
import ipyleaflet
import ipywidgets as widgets
from traitlets import All
from ipywidgets import (Widget, HBox, VBox, Text, Textarea, Dropdown,
                        Button, Layout, Tab, Image, HTML)
from typing import Dict, Tuple, List, Union, Optional, Any, Callable

from .extendedtab import ExtendedTab
from .responseviews import RawResponseView, ResponseView, builtin_view_classes


# default recorder
recorder = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='fixtures/cassettes',
    record_mode='new_episodes',
    match_on=['uri', 'method'],
)


class MyLogger(object):
    def __init__(self):
        # Create the Logger
        self.logger = logging.getLogger('ipyrest')
        self.logger.setLevel(logging.INFO)

        # Create the Handler for logging data to a file
        logger_handler = logging.FileHandler('ipyrest.log')
        logger_handler.setLevel(logging.INFO)

        # Create a Formatter for formatting the log messages
        logger_formatter = logging.Formatter(
            '%(asctime)-15s - %(name)s - %(levelname)s - %(message)s')

        # Add the Formatter to the Handler
        logger_handler.setFormatter(logger_formatter)

        # Add the Handler to the Logger
        self.logger.addHandler(logger_handler)
        self.logger.info('Completed configuring logger!')

        # def __del__(self):
        #     self.logger.info('Shutting down logger...')


def execute_request(url: str,
                    method: str = 'get',
                    headers: Dict = {},
                    params: Dict = {},
                    json: Dict = {},

                    recorder: Optional[vcr.VCR] = recorder,
                    cassette_path: str = '',
                    logger: Optional[MyLogger] = None) -> Tuple[requests.models.Response, bool]:
    """
    Execute a HTTP request and return response defined by the `requests` package.
    """
    if logger:
        logger.logger.info(
            'execute_request {} {}'.format(recorder, cassette_path))

    is_cached = False
    method_func = requests.__getattribute__(method.lower())
    if cassette_path and recorder:
        from vcr.cassette import Cassette
        from vcr.request import Request
        logger.logger.info('imported vcr')
        req = Request(method.upper(), url,
                      'irrelevant body?', {'some': 'header'})
        logger.logger.info('req ' + str(req))
        c_path = os.path.join(recorder.cassette_library_dir, cassette_path)
        logger.logger.info(c_path)
        logger.logger.info(Cassette(None).load(path=c_path))
        if req in Cassette(None).load(path=c_path):
            is_cached = True
        with recorder.use_cassette(c_path):
            logger.logger.info('running...')
            if json:
                resp = method_func(url, headers=headers, params=params, json=json)
            else:
                resp = method_func(url, headers=headers, params=params)
            logger.logger.info('got it...')
    else:
        if json:
            resp = method_func(url, headers=headers, params=params, json=json)
        else:
            resp = method_func(url, headers=headers, params=params)
    # FIXME: requests.post('http://httpbin.org/post', json={"key": "value"})
    return resp, is_cached


def mask_credentials(text: str, field_names: List[str]) -> str:
    "Mask out credentials params in a string, here an URL query string."

    for name in field_names:
        text = re.sub(f'{name}=[\-\w]+', f'{name}=******', text)
    return text


def update_qs(url, **kwargs):
    "Update parameters in URL query string as given in kwargs."

    # values in kwargs must be lists containing at least one string
    query_dct = parse_qs(urlparse(url).query)
    query_dct.update(kwargs)
    qs_new = '&'.join('{}={}'.format(k, v[0]) for (k, v) in query_dct.items())
    url_parts = list(urlparse(url))
    url_parts[4] = qs_new
    new_url = urlunparse(url_parts)
    return new_url


class Api(VBox):
    """
    Return a widget that mimics a Postman-like interface for exploring APIs.
    """

    def __init__(self,
                 url: str = '',
                 method: str = 'get',
                 args: Dict = {},
                 params: Dict = {},
                 data: Dict = {},
                 headers: Dict = {},
                 cookies: Dict = {},

                 click_send: bool = False,
                 timeout: float = 10,
                 cassette_path: str = '',
                 views: List[ResponseView] = builtin_view_classes,
                 additional_views: List[ResponseView] = [],
                 post_process_resp: Optional[Callable] = None,
                 config=None) -> None:  # FIXME: use config
        """
        Build widget layout and wire its components.
        """
        super().__init__()

        self.url = url
        self.method = method
        self.args = args
        self.params = params
        self.data = data
        self.headers = headers
        self.cookies = cookies

        self.timeout = timeout
        self.cassette_path = cassette_path

        self.views = views + additional_views
        self.viewers = OrderedDict({})
        self.post_process_resp = post_process_resp
        self.logger = MyLogger()

        lt_w100p = Layout(width='100%')  # , height='100px')
        lt_w100px = Layout(width='100%px')

        # top input line with URL field
        opts = 'GET POST PUT PATCH DELETE HEAD OPTIONS'.split()
        self.method_ddn = Dropdown(
            options=opts,
            value=method.upper(),
            layout=lt_w100px)
        self.url_txt = Text(layout=lt_w100p)
        self.req_btn = Button(description='REQ', tooltip='Show Request Pane')
        self.rep_btn = Button(description='REP', tooltip='Show Response Pane')
        self.send_btn = Button(
            description='Send', tooltip='Send request', button_style='primary')
        self.input_hbx = HBox([
            self.method_ddn,
            self.url_txt,
            self.req_btn,
            self.rep_btn,
            self.send_btn],
            layout=lt_w100p)

        # request pane
        self.showing_req_pane = False
        self.req_pane = ExtendedTab()
        self.req_pane.add_child_named(VBox(), 'Arguments')
        self.req_pane.add_child_named(VBox(), 'Parameters')
        headers_ta = Textarea(layout=lt_w100p)
        if headers:
            headers_ta.value = json.dumps(headers, indent=2)
        self.req_pane.add_child_named(headers_ta, 'Headers')
        data_ta = Textarea(layout=lt_w100p)
        if data:
            data_ta.value = json.dumps(data, indent=2)
        self.req_pane.add_child_named(data_ta, 'Data')
        self.req_pane.selected_index = None

        # response pane
        self.content_area = ExtendedTab()
        self.content_area.add_child_named(Textarea(layout=lt_w100p), 'Raw')
        self.content_area.selected_index = None

        self.showing_rep_pane = False
        self.resp_pane = ExtendedTab()
        self.resp_pane.selected_index = None
        self.resp_pane.add_child_named(self.content_area, 'Content')
        self.resp_pane.add_child_named(Textarea(layout=lt_w100p), 'Headers')
        self.resp_pane.add_child_named(Textarea(layout=lt_w100p), 'Cookies')

        # interactions
        self.req_btn.on_click(self.req_clicked)
        self.rep_btn.on_click(self.rep_clicked)
        self.send_btn.on_click(self.send_clicked)
        self.url_txt.observe(self.url_changed, names='value')

        # top level UI
        self.req_htm = HTML('Request')
        self.resp_status_htm = HTML('???', layout=Layout(width='100%'))
        self.resp_htm = HBox([HTML('Response')])
        ui_kids = [self.input_hbx]
        if self.showing_req_pane:
            ui_kids += [self.req_htm, self.req_pane]
        if self.showing_rep_pane:
            ui_kids += [self.resp_htm, self.resp_pane]
        self.children = ui_kids

        # fill in default arguments and parameters if given
        if url:
            if args:
                url = url.format(**args)
            if params:
                query = '&'.join(f'{k}={v}' for (k, v) in params.items())
                url = f'{url}?{query}'
            self.url_txt.value = url

        self.req_pane.get_child_named('Arguments').children = \
            [Text(description=key, value=args[key]) for key in args]
        param_texts = [Text(description=key, value=params[key]) for key in params]
        for pt in param_texts:
            pt.observe(self.param_changed, names=All)

        self.req_pane.get_child_named('Parameters').children = param_texts

        # finally, click send button if desired
        if click_send:
            self.click_send()

    def url_changed(self, change) -> None:
        "Callback to be called when the input URL is changed."

        value = change['new']
        try:
            q = splitquery(value)[1]
        except AttributeError:
            return
        params = parse_qs(q)
        self.req_pane.get_child_named('Parameters').children = \
            [Text(description=key, value=params[key][0]) for key in params]

    def param_changed(self, change) -> None:
        "Callback to be called when an input parameter is changed."

        self.logger.logger.info('old url {}'.format(self.url_txt.value))
        key = change['owner'].description
        value = change['new']
        new_url = update_qs(self.url_txt.value, **{key: [value]})
        self.url = new_url
        self.url_txt.value = new_url
        self.logger.logger.info('param_changed {} {}'.format(key, value))
        self.logger.logger.info('new url {}'.format(self.url_txt.value))

    def click_send(self) -> None:
        "Programmatically click on Send button."

        self.send_btn._click_handlers(self.send_btn)

    def update_ui(self) -> None:
        "Update entire UI, drawing and hiding what is needed/not needed."

        kids = [self.input_hbx]
        if self.showing_req_pane:
            kids += [self.req_htm, self.req_pane]
        if self.showing_rep_pane:
            kids += [self.resp_htm, self.resp_pane]
        self.children = tuple(kids)

    def req_clicked(self, btn: Button) -> None:
        "Callback to be called when the Request button is clicked."

        self.showing_req_pane = not self.showing_req_pane
        self.update_ui()
        btn.tooltip = 'Hide Request Pane' if self.showing_req_pane else 'Show Request Pane'

    def rep_clicked(self, btn: Button) -> None:
        "Callback to be called when the Response button is clicked."

        self.showing_rep_pane = not self.showing_rep_pane
        self.update_ui()
        btn.tooltip = 'Hide Response Pane' if self.showing_rep_pane else 'Show Response Pane'

    def send_clicked(self, btn: Button) -> None:
        "Callback to be called when the Send button is clicked."

        btn.button_style = 'info'
        btn.disabled = True
        self.logger.logger.info('clicked')
        url = self.url_txt.value
        method = self.method_ddn.value

        headers_text = self.req_pane.get_child_named('Headers').value
        headers = json.loads(headers_text) if headers_text.strip() else {}

        data_text = self.req_pane.get_child_named('Data').value
        data = json.loads(data_text) if data_text.strip() else {}

        args = [url, method]
        kwargs = dict(headers=headers,
                      cassette_path=self.cassette_path, logger=self.logger)
        if data:
            kwargs['json'] = data
        self.logger.logger.info('vcr request {} {}'.format(args, kwargs))
        if 1:
            timeout_execute_request = timeout_decorator.timeout(
                self.timeout)(execute_request)
            try:
                self.logger.logger.info('callign timeout_execute_request')
                self.resp, is_cached = timeout_execute_request(*args, **kwargs)
                self.logger.logger.info('result request {}'.format(self.resp))
            except timeout_decorator.TimeoutError:
                self.logger.logger.info('timed out')
                self.resp_htm = HBox([
                    HTML('Response'),
                    HTML('Status: Timed out after {:.3f} secs.'.format(
                        self.timeout))
                ],
                    layout=Layout(width='100%', justify_content='space-between'))
                raise
        else:
            self.resp, is_cached = execute_request(*args, **kwargs)
        self.logger.logger.info(self.resp.content)

        if self.post_process_resp:
            self.post_process_resp(self.resp)
        btn.button_style = 'primary'
        self.show_response(self.resp, is_cached)
        btn.disabled = False

    def show_response(self,
                      resp: requests.models.Response,
                      is_cached: bool,
                      views: Optional[List[ResponseView]] = None) -> None:
        "Show the HTTP response in various response UI elements."

        self.logger.logger.info('response ' + str(resp.headers))

        content_tab = self.resp_pane.get_child_named('Content')

        # Raw tab
        viewer = RawResponseView()
        self.logger.logger.info('0')
        viewer.render(resp)
        self.logger.logger.info('0')
        self.viewers['Raw'] = viewer
        try:
            content_tab.get_child_named('Raw').value = \
                str(resp.content.decode(resp.encoding)) \
                if resp.encoding else str(resp.content)
        except UnicodeDecodeError:
            content_tab.get_child_named('Raw').value = str(resp.content)
        content_tab.select_child_named('Raw')
        sorted_header_items = OrderedDict(
            sorted(OrderedDict(resp.headers).items()))
        headers_ta = self.resp_pane.get_child_named('Headers')
        headers_ta.value = json.dumps(sorted_header_items, indent=2)
        num_lines = headers_ta.value.count('\n')
        headers_ta.rows = min(10, num_lines + 1)
        self.resp_pane.get_child_named(
            'Cookies').value = str(resp.cookies.items())

        content_type = resp.headers['Content-Type']
        maintype, subtype, params = re.match(
            '(\w+)/([\.\+\-\w]+)(;.*)?', content_type).groups()
        essence = f'{maintype}/{subtype}'
        self.logger.logger.info(
            f'maintype: {maintype}, subtype: {subtype}, params: {params}')
        self.logger.logger.info(f'essence: {essence}')
        self.resp_pane.selected_index = 0
        self.showing_rep_pane = True

        # status
        kwargs = dict(
            code=resp.status_code,
            reason=resp.reason,
            encoding=resp.encoding,
            elapsed='{:.3f}'.format(resp.elapsed.total_seconds()),
            # length=resp.headers['Content-Length'],
            length=resp.headers.get('Content-Length', '?'),
            cached=is_cached
        )
        self.resp_htm = HBox([
            HTML('Response'),
            HTML(('Status: {code}/{reason}, Encoding: {encoding}, '
                  'Time: {elapsed} secs, Length: {length} Bytes, Cached: {cached}').format(**kwargs))
        ],
            layout=Layout(width='100%', justify_content='space-between'))

        # find views able to render the response and add their results to the tab
        for ViewClass in views or self.views:
            name = ViewClass.name
            self.logger.logger.info(f'{name}')
            for mt_pat in ViewClass.mimetype_pats:
                self.logger.logger.info(f'{mt_pat} {essence}')
                if re.match(mt_pat, essence):
                    self.logger.logger.info(f'{essence}')
                    viewer = ViewClass(owner=self)
                    self.viewers[name] = viewer
                    res = viewer.render(resp)
                    self.logger.logger.info('data {}'.format(str(viewer.data)))
                    self.logger.logger.info('rendered')
                    if res:
                        content_tab.add_child_named(res, ViewClass.name)
                        content_tab.select_child_named(ViewClass.name)
                else:
                    self.logger.logger.info('skipped')

        self.update_ui()

    # FIXME: add a button to eventually call this
    def clear_all(self):
        "Clear the request and response UI elements."

        # input line should likely not be cleared
        # self.url_txt.value = ''

        # request pane
        get = self.req_pane.get_child_named
        get('Arguments').children = tuple()
        get('Parameters').children = tuple()
        get('Headers').value = ''
        get('Data').value = ''

        # repsonse pane
        get = self.resp_pane.get_child_named
        get('Content').get_child_named('Raw').value = ''
        get('Headers').value = ''
        get('Cookies').value = ''
        content_tab = get('Content')
        for title in content_tab.children_dict.keys():
            if title != 'Raw':
                content_tab.remove_child_named(title)
