from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
app_name = 'blog'

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/done/$', views.index, name='index'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^sendmail/$', views.mail, name='mail'),
]













