from django.conf.urls import url

from . import views

app_name = 'frutaui'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^more$', views.more, name='more'),
    # url(r'^todavia$', views.index, name='index'),
]