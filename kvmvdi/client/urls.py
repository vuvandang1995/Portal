from django.conf.urls import include, url
from django.urls import path
from . import views

app_name = 'client'
urlpatterns = [
    path('', views.home, name='home'),
    path('/instances', views.instances, name='instances'),
    path('/networks', views.networks, name='networks'),
    path('/sshkeys', views.sshkeys, name='sshkeys'),
    path('/volumes', views.volumes, name='volumes'),
    path('/show_instances/<str:serverid>', views.show_instances, name='show_instances'),
    path('/profile', views.user_profile, name='profile'),
    path('/oders', views.user_oders, name='oders'),
    path('/logout', views.user_logout, name='logout'),
    path('/home_data_', views.home_data, name='home_data'),

]
