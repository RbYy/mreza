"""mreza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from mreza import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mreza/', views.mreza, name='mreza'),
    url(r'^shrani/', views.shrani, name='shrani'),
    url(r'^ustvari_mrezo/', views.ustvari_mrezo, name='ustvari_mrezo'),
    url(r'^povleci_mreze/', views.povleci_mreze, name='povleci_mreze'),
    url(r'^odjava', views.odjava, name='odjava'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
]
