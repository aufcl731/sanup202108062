from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'design_data'
urlpatterns = [
    url(r'^activeUser$', views.activeUser),
    url(r'^companyInfo$', views.companyInfo),
    url(r'^changePassword$', views.changePassword),
    url(r'^changeUserInfo$', views.changeUserInfo),
    url(r'^getAddress', views.getAddress),
    url(r'^userdetailtest/(?P<id>\d+)$', views.usetdetailtest),
    url(r'^userupdate$', views.userupdates),
    url(r'^userdel$', views.userdel),
    url(r'^accountadd$',views.accountadd),
    url(r'^accountselect$', views.accountselect),
    url(r'^accountmodify$', views.accountmodify),
    url(r'^accountdel$',views.accountdel),
    url(r'^languagech$',views.langch),
    url(r'^', csrf_exempt(views.setting)),
]