from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from design_data import views
app_name = 'design_data'
urlpatterns = [
    url(r'^upload$', csrf_exempt(views.upload)),
    url(r'^designdata$', csrf_exempt(views.designDataByJson)),
    url(r'^delete', csrf_exempt(views.delete)),
    url(r'^getList', csrf_exempt(views.designListByJson)),
    url(r'^detail/(?P<designId>\d+)', views.showDesign),
    url(r'^design/(?P<designId>\d+)', views.showDesignProduction),
    url(r'^', csrf_exempt(views.showList)),
]