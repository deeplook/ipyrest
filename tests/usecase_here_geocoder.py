import os
from urllib.parse import quote
from ipyrest import Api
url = 'https://geocoder.api.here.com/6.2/geocode.json'
params = dict(
    searchtext=quote('Invalidenstr. 116, 10115 Berlin, Germany'),
    app_id=os.getenv('HEREMAPS_APP_ID'),
    app_code=os.getenv('HEREMAPS_APP_CODE')
)
api = Api(url, params=params, click_send=True)
