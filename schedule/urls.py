from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from . import views
from rest_framework import routers

router2 = routers.DefaultRouter()
router2.register(r'knit_process', views.Knit_process_api)
router3 = routers.DefaultRouter()
router3.register(r'warp_process', views.Warp_process_api)

app_name = 'schedule'

urlpatterns = [
    url(r'^getMachineByDate$', csrf_exempt(views.getMachineByDate)),
    url(r'^getMaterialByDate$', csrf_exempt(views.getMaterialByJson)),
    url(r'^process$', views.getProcessByJson),
    url(r'^createSchedule$', views.createSchedule),
    url(r'^selectOrder$', views.selectOrder),
    url(r'^saveBeam$', views.saveBeam),
    url(r'^$', csrf_exempt(views.showSchedule)),
    url(r'^knit_process_api/', include(router2.urls, 'knit_process_api'), name='knit_process_api'),
    url(r'^warp_process_api/', include(router3.urls, 'warp_process_api'), name='warp_process_api'),
]