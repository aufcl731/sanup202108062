from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'design_data'
urlpatterns = [
    url(r'^activeUser$', views.activeUser),
    url(r'^companyInfo$', views.companyInfo),
    url(r'^createDepartment$', views.createDepartment),
    url(r'^changePassword$', views.changePassword),
    url(r'^changeUserInfo$', views.changeUserInfo),
    url(r'^getAddress', views.getAddress),
    #url(r'^ordercheack$', views.ordercheack),
    url(r'^', csrf_exempt(views.setting)),
]