from django.conf.urls import url

from blogHome import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^test/$', views.test),
]