"""
Ipyrest tests for the code generation feature.

To be executed with pytest:

    pytest -s -v test_codegen.py
"""


def test_py_req_template_config():
    """Test create Python code with requests template from config."""

    from ipyrest.codegen import create_code, python_requests_template
    config = dict(
        method='POST',
        url='http://apple.com',
        headers={'X-Foo': 'foo.bar'},
        params={'foo': '42'},
        data='XXX'
    )
    snippet = create_code(python_requests_template, config)

    # Test if correct assignements are contained in the snippet
    assert "method = '{method}'".format(**config) in snippet
    assert "url = '{url}'".format(**config) in snippet
    assert "headers = {headers}".format(**config) in snippet
    assert "params = {params}".format(**config) in snippet
    assert "data = '{data}'".format(**config) in snippet


def test_py_req_template_api():
    """Test create Python code with requests from Api instance."""

    from ipyrest import Api
    from ipyrest.codegen import create_code_from_api, python_requests_template
    config = dict(
        url = 'http://apple.com',
        method='POST',
        headers={'X-Foo': 'foo.bar'},
        params={'foo': '42'},
        # data='XXX'
    )
    api = Api(**config)
    snippet = create_code_from_api(python_requests_template, api)

    # Test if correct assignements are contained in the snippet
    assert "method = '{method}'".format(**config) in snippet
    assert "url = '{url}'".format(**config) in snippet
    assert "headers = {headers}".format(**config) in snippet
    assert "params = {params}".format(**config) in snippet
    # assert "data = '{data}'".format(**config) in snippet
