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
from mreza.views import shrani_nove_koordinate_batimenta

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mreza/', views.mreza, name='mreza'),
    url(r'^ustvari_batiment/', views.ustvari_batiment, name='ustvari_batiment'),
    url(r'^zbrisi_batiment/', views.zbrisi_batiment, name='zbrisi_batiment'),
    url(r'^shrani_nove_koordinate_batimenta/', shrani_nove_koordinate_batimenta, name='shrani_nove_koordinate_batimenta'),
    url(r'^ustvari_mrezo/', views.ustvari_mrezo, name='ustvari_mrezo'),
    url(r'^povleci_mreze/', views.povleci_mreze, name='povleci_mreze'),
    url(r'^poslji_komplet/', views.poslji_komplet, name='poslji_komplet'),
    url(r'^shrani_nove_dimenzije_mreze/', views.shrani_nove_dimenzije_mreze, name='shrani_nove_dimenzije_mreze'),
    url(r'^odjava', views.odjava, name='odjava'),
    url(r'^aktiviraj_drugo_mrezo/', views.aktiviraj_drugo_mrezo, name='aktiviraj_drugo_mrezo'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
]
