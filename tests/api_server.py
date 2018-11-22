#!/usr/bin/env python

"""
A simple HTTP server implementing a minimal RESTful API for testing ipyrest.
"""

import json
import time

from flask import Flask, Response, request, jsonify, send_file


app = Flask(__name__)


# get html
# get json
# get geojson
# get xml
# get image

# path params
# query params
# post data
# mime-type
# file upload

# request.method == 'POST'
# request.args
# request.data
# ...


# In the app routes below, without any methods parameter the default one is 'GET'.


# GET

@app.route('/')
def home() -> str:
    resp = Response('')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/head', methods=['HEAD'])
def head() -> str:
    resp = app.make_response('')
    resp.mimetype = "text/plain"
    return resp


@app.route('/get_json')
def get_json() -> str:
    obj = {'foo': 23, 'bar': 'b a r'.split()}
    return jsonify(obj)


@app.route('/get_json_param/<int:param>')
def get_json_param(param: int) -> str:
    obj = {'foo': 'bar', 'param': param}
    return jsonify(obj)


@app.route('/get_json_query/')
def get_json_query() -> str:
    args = request.args
    return jsonify(args)


@app.route('/post_json_data/', methods=['POST'])
def post_json_data() -> str:
    data = request.data
    print(data)
    return jsonify(data)


@app.route('/get_json_3d/')
def get_json_3d() -> str:
    import numpy as np
    x, y, z = np.random.random((3, 100))
    data = dict(x=x.tolist(), y=y.tolist(), z=z.tolist())
    return jsonify(data)


@app.route('/get_image')
def get_image() -> str:
    # if request.args.get('type') == '1':
    filename = 'jupyter.jpg'
    return send_file(filename, mimetype='image/jpeg')


@app.route("/get_header")
def get_header() -> str:
    resp = Response("Foo bar baz")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/get_header_echo")
def get_header_echo() -> str:
    return jsonify(dict((k, v) for (k, v) in request.headers.items()))


@app.route('/get_mimetype')
def get_mimetype() -> str:
    xml = '<xml>foo</xml>'
    resp = app.make_response(xml)
    resp.mimetype = "text/xml"
    return resp


@app.route('/get_slow/sleep/<float:period>')
def get_slow(period: float) -> str:
    time.sleep(period)
    return f'Sorry for being {period} seconds late!'


@app.route('/get_protobuf')
def get_protobuf() -> str:
    person_ser = b'\n\x08John Doe\x10\xd2\t\x1a\x10jdoe@example.com"\x0c\n\x08555-4321\x10\x01'
    resp = app.make_response(person_ser)
    resp.mimetype = "application/x-protobuf"
    return resp


@app.route('/get_protobuf/person/<int:id>')
def get_protobuf_person(id: int) -> str:
    import addressbook_pb2

    with open('addressbook_pb', "rb") as f:
        address_book = addressbook_pb2.AddressBook()
        address_book.ParseFromString(f.read())

    person = None
    for per in address_book.people:
        if per.id == id:
            break

    person_ser = person.SerializePartialToString() if person else b''

    resp = app.make_response(person_ser)
    resp.mimetype = "application/x-protobuf"
    return resp


@app.route('/get_svg')
def get_svg() -> str:
    resp = app.make_response(open('Cuba.svg').read())
    resp.mimetype = "image/svg+xml"
    return resp


gpx_body = '''\
<?xml version="1.0"?>
<gpx version="1.0"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns="http://www.topografix.com/GPX/1/0"
xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">
  <trk>
    <trkseg>
      <trkpt lat="51.10177" lon="0.39349"/>
      <trkpt lat="51.10181" lon="0.39335"/>
      <trkpt lat="51.10255" lon="0.39369"/>
      <trkpt lat="51.10398" lon="0.39466"/>
      <trkpt lat="51.10501" lon="0.39533"/>
    </trkseg>
  </trk>
</gpx>
'''
# gpx_body = open('/Volumes/SanDisk128/mobiledev/src/projects/herestapis_comtravo/data/bus_ride.gpx').read()
@app.route('/get_gpx')
def get_gpx() -> str:
    resp = app.make_response(gpx_body)
    resp.mimetype = "application/gpx+xml"
    return resp


# POST

@app.route("/post_data_echo", methods=['POST'])
def post_data_echo() -> str:
    return jsonify(json.loads(request.data.decode('utf-8')))


# Multi-method

@app.route('/echo/<path:subpath>', methods=['HEAD', 'GET', 'POST'])
def echo(subpath: str) -> str:
    "Echo everything we can inside as a JSON result."
    return jsonify(dict(
        method=request.method,
        headers=request.headers,
        args=request.args,
        params=request.params,
        data=request.data,
    ))


if __name__ == "__main__":
    app.run(debug=True)
