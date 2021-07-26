"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from account import views
from config import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^pjs1234', views.pjs1234),
    url(r'^$', views.login_site, name='login_site'),
    url(r'^server/', views.server, name='server'),
    url(r'^signup', views.signUo, name='signup'),
    url(r'^logout', views.logout_site, name='logout_site'),
    url(r'^design_data/', include('design_data.urls', namespace='design_data')),
    url(r'^order/', include('order.urls', namespace='order')),
    url(r'^setting/', include('setting.urls', namespace='setting')),
    url(r'^material/', include('materials.urls', namespace='material')),
    url(r'^schedule/', include('schedule.urls', namespace='schedule')),
    url(r'^machine/', include('machine.urls', namespace='machine')),
    url(r'^production/', include('production.urls', namespace='production')),
    #url(r'^ordercheack$', views.ordercheack),
]



urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)