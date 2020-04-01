from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from schedule import views
app_name = 'schedule'
urlpatterns = [
    url(r'^getMachineByDate', csrf_exempt(views.getMachineByDate)),
    url(r'^getMaterialByDate', csrf_exempt(views.getMaterialByJson)),
    url(r'^process', views.getProcessByJson),
    url(r'^createSchedule', views.createSchedule),
    url(r'^selectOrder', views.selectOrder),
    url(r'^saveBeam', views.saveBeam),
    url(r'^', csrf_exempt(views.showSchedule)),
]