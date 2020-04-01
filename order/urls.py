from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views
app_name = 'order'

urlpatterns = [
    url(r'^rawroll$', views.rawroll),
    url(r'^warpWorkSheet', views.warpTable),
    url(r'^modify$', views.modifyOrder),
    url(r'^delete$', views.delete),
    url(r'^$', views.order),
    url(r'^list$', views.getOrderListByJson),
    url(r'^detail/(?P<orderId>\d+)', views.getOrderByJson),
    url(r'^showQr/(?P<id>\d+)', views.showQr),
    url(r'^subOrderJson/(?P<id>\d+)', views.getSubOrderByJson),
    url(r'^ordercheack$', views.ordercheack),
]