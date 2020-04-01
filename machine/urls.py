from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from machine import views
app_name = 'machine'
urlpatterns = [
    url(r'^$', csrf_exempt(views.showMachine)),
    url(r'^setmachine', csrf_exempt(views.setMachine)),
    url(r'^listByType', csrf_exempt(views.listByType)),
    url(r'^getWarpInfoByJson', csrf_exempt(views.getWarpInfoByJson)),
    url(r'^getKnitInfoByJson', csrf_exempt(views.getKnitInfoByJson)),
    url(r'^setKnitMachine', csrf_exempt(views.setKnitMachine)),
    url(r'^setWarpMachine', csrf_exempt(views.setWarpMachine)),
    url(r'^deleteWarpMachine', csrf_exempt(views.deleteWarpMachine)),
    url(r'^deleteKnitMachine', csrf_exempt(views.deleteKnitMachine)),
    #url(r'^ordercheack$', views.ordercheack),
]