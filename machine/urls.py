from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from machine import views
from rest_framework import routers
app_name = 'machine'

router4 = routers.DefaultRouter()
router4.register(r'knit_machine', views.Knit_machine_api, basename='knit_machine_apis')
router5 = routers.DefaultRouter()
router5.register(r'warp_machine', views.Warp_machine_api, basename='warp_machine_apis')

urlpatterns = [
    url(r'^$', csrf_exempt(views.showMachine)),
    url(r'^setmachine$', csrf_exempt(views.setMachine)),
    url(r'^listByType$', csrf_exempt(views.listByType)),
    url(r'^getWarpInfoByJson$', csrf_exempt(views.getWarpInfoByJson)),
    url(r'^getKnitInfoByJson$', csrf_exempt(views.getKnitInfoByJson)),
    url(r'^setKnitMachine$', csrf_exempt(views.setKnitMachine)),
    url(r'^setWarpMachine$', csrf_exempt(views.setWarpMachine)),
    url(r'^deleteWarpMachine$', csrf_exempt(views.deleteWarpMachine)),
    url(r'^deleteKnitMachine$', csrf_exempt(views.deleteKnitMachine)),
    url(r'^knit_machine_api/', include(router4.urls, 'knit_machine_api'), name='knit_machine_api'),
    url(r'^warp_machine_api/', include(router5.urls, 'warp_machine_api'), name='warp_machine_api'),
    #url(r'^ordercheack$', views.ordercheack),
]