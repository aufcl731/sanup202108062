from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers

from design_data import views
app_name = 'design_data'

router = routers.DefaultRouter()
router.register(r'design_data_api', views.Design_data_api, basename='design_data_apis')

urlpatterns = [
    url(r'^upload$', csrf_exempt(views.upload)),
    url(r'^designdata$', csrf_exempt(views.designDataByJson)),
    url(r'^delete$', csrf_exempt(views.delete)),
    url(r'^getList$', csrf_exempt(views.designListByJson)),
    url(r'^detail/(?P<designId>\d+)$', views.showDesign),
    url(r'^design/(?P<designId>\d+)$', views.showDesignProduction),
    url(r'^$', csrf_exempt(views.showList)),
    url(r'^design_data_api/', include(router.urls, 'Design_data_api'), name='Design_data_api'),
]