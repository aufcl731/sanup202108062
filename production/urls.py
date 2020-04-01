from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views
app_name = 'production'

urlpatterns = [
    url(r'^process/(?P<pk>\d+)', views.productionDetail, name='process_detail'),
    #
    url(r'^detail/(?P<productionId>\d+)', views.showDesignProduction),
    url(r'^$', views.production),
]