from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from materials import views
app_name = 'material'
urlpatterns = [
    url(r'^yarnDelete$', views.yarnDelete),
    url(r'^beamDelete$', views.beamDelete),
    url(r'^greigeDelete$', views.greigeDelete),
    url(r'^createBeam$', views.createBeam),
    url(r'^createYarn$', views.createYarn),
    url(r'^createroll$', views.createRoll),
    url(r'^getYarnInfoByJson$', views.getYarnInfoByJson),
    url(r'^searchYarn$', views.searchYarn),
    url(r'^searchBeam$', views.searchBeam),
#    url(r'^createRaw$',views.createRaw, name='createRaw'),
    url(r'^', csrf_exempt(views.showMaterial)),
]