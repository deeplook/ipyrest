Ipyrest
=======

[![Binder](https://mybinder.org/badge_logo.svg)](http://beta.mybinder.org/v2/gh/deeplook/ipyrest/master) 
[![Nbviewer](https://github.com/jupyter/design/blob/master/logos/Badges/nbviewer_badge.svg)](http://nbviewer.jupyter.org/github/deeplook/ipyrest/tree/master/)
[![Travis-CI](http://img.shields.io/travis/deeplook/ipyrest.svg)](https://travis-ci.org/deeplook/ipyrest)
[![image](https://img.shields.io/pypi/pyversions/ipyrest.svg)](https://pypi.org/project/ipyrest/)
[![image](https://img.shields.io/pypi/v/ipyrest.svg)](https://pypi.org/project/ipyrest/)
[![image](https://img.shields.io/pypi/l/ipyrest.svg)](https://pypi.org/project/ipyrest/)
  
Ipyrest is an emerging Jupyter notebook widget for exploring RESTful APIs. It has two main goals: provide a more convenient interface in the spirit of Postman, and allow for plug-in components, starting with output renderers for various MIME types, e.g. GeoJSON:

![banner](https://github.com/deeplook/ipyrest/blob/master/images/banner.png "")

Features
--------

Ipyrest deals with the following concepts, implemented to varying degrees: HTTP Server, Service, Request, Response, Data, MIME-Types, Compression, Logging, Caching, Time-Outs, Errors, Views, Plugins, Testing, and UI.

At the moment the following plugins are available for rendering output from HTTP responses in common formats: Plain Text, CSV, HTML, Bitmaps, SVG, JSON, GeoJSON, GPX, Protobuf, (and some experimental 3D stuff).

The main dependencies are: Python >= 3.6, jupyter, ipywidgets, timeout_decorator, requests, and vcr. Plugin dependencies are: ipyleaflet, ipyvolume, geojson, qgrid, protobuf. Testing dependencies are flask, mypy, and pytest.

Installation
------------

Released versions of Ipyrest can be installed from PyPI with:

``` {.sourceCode .bash}
pip install ipyrest
```

Development versions of Ipyrest can be installed either directly from GitHub or after downloading/cloning and unpacking like this in its top-level directory:

``` {.sourceCode .bash}
pip install git+https://github.com/deeplook/ipyrest

pip install -e .
```

Testing
-------

Run `pip install -r requirements_test.txt` and `PYTHONPATH=. pytest -s -v tests` in the root directory. Some tests will automatically start a local flask webserver in `tests/api_server.py` which implements a set of sample API endpoints for local testing. And some of these tests need keys/tokens defined as environment variables for the respective APIs being tested. If not present these tests will be skipped.

Documentation
-------------

The `docs` folder is only a stub for now. At the moment it is recommended to look at [`examples/meetup.ipynb`](examples/meetup.ipynb), mostly a tutorial-like collection of examples given as a presentation at a meetup. Some of these need appropriate API keys.

How to Contribute
-----------------

More to come...
