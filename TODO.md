# TODO

This is a slightly Postman-like Jupyter widget for exploring RESTful APIs.

More to come...

To-do:

- handle compression
- show when errors occur
- add real gists with 3D data (simple and Lidar-like)
- pass entire vcr recorder object instead of a cassette path to make config easier
- use type hints for signatures (except for JSON, use Any there)
- test URLs with encoded params like https://foo.com/search?q=search%20index%3D
- use/show/test request/response cookies
- create something like a RequestView class with some UI for the input
- use sliders in addition to text fields for numerical request parameters
- use dropdown boxes in addition to text fields for categorial request parameters
- mask request query params with specific names (makes the interface a little useless...)
- add clear button to response pane
- add more tests, accessing various types of response output and views derived from it
- concentrate init params for Api class into configuration object
- describe init params in Api class' decstring
- learn more from https://github.com/oschuett/appmode to add an even better binder integration

Done:

- add working mybinder.org badge
- add working nbviewer badge
- add info to status line if request response was read from cache (`vcr` cassette) 
- add test using mypy on some parts of the code
- access result data rendered in response view (built-in or custom)
- use caching based on `vcr` package
- add basic example for 3D data using ipyvolume widget
- show a status line with HTTP code, reason, time, encoding
- add test/example for content-type application/x-protobuf
  - https://stackoverflow.com/questions/19734617/protobuf-to-json-in-python
  - https://developers.google.com/protocol-buffers/docs/proto3#json
- show SVG
- indicate when a timeout occurs
- improve coding, e.g. better identifier names
- use timeouts when executing a request
- use request headers
- use request data (JSON)
- provide ExtendedTab class as subclass of Tab to access children by name
- change module name to ipyrest
- rename package to `ipyrest`
- class `__init__` constructor has url, params, headers, cookies
- distinguish between path params and query params
- show bitmaps tab for respective content-type in response header
- show GeoJSON tab for respective content-type in response header
- calculate sppropriate center and zoom level for shown GeoJSON data
- show HTML tab (only basic HTML, no CSS/JS)
- provide a test-suite for testing the widgets programmatically (no browser needed)
- implement views to render specific mime-types
- allow for customized response views (e.g. show a route from the HERE API)
- support GPX format (XML)

Mabye:

- import Postman collections files
- use/store environments like Postman
- keep history of sent requests/responses and allow to repeat them (some dropdown menu?)
- add search field for JSON output
- add search field for XML output
- use pygments for styling HTML widgets (unclear if supported by ipywidgets for now)
- find some MIMEType class like this: https://github.com/jsdom/whatwg-mimetype, see also https://tools.ietf.org/html/rfc2231
