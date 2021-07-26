# -*- coding: utf-8 -*-
import urllib
import urllib
from urllib.parse import urlencode

import urllib3
from requests import request


def url_image_upload(josic_imgpath,josicimg,Magnification_imgpath,Magnification_img, name):
   data = {
        'josic_imgpath': josic_imgpath,
        'josicimg' : josicimg,
        'Magnification_imgpath' : Magnification_imgpath,
        'Magnification_img' : Magnification_img,
        'name' : name
   }
   http = urllib3.PoolManager()

   reselt = http.request('POST', 'http://211.238.177.146:8888/upload?' + urlencode(data))
   return reselt
