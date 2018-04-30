from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),    
    url(r'^panelControl', views.panelControl, name='panelControl'),
    url(r'^dataResult', views.dataResult, name='dataResult'),

]