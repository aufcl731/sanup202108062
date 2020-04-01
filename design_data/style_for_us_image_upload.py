# -*- coding: utf-8 -*-
import urllib
#import urllib2
from urllib.parse import urlencode

import urllib3

def style_for_us_image_upload(image_path, image_name):
    data = {
        'image_path': image_path,
        'image_name': image_name,
    }
    http = urllib3.PoolManager()

    # style for us 로 전달
    reselt = http.request('GET', 'http://stylefor.us/texddm_image_upload?' + urlencode(data))
    return reselt