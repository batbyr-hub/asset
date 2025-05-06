"""asset URL Configuration

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
from django.urls import path, re_path, include
from django.contrib import admin

from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from controller import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", views.login),
    path("nuur/", views.nuur),

    path('asset/niitShaardah/', views.niitShaardah),
    path('asset/huleegdejBaigaa/', views.huleegdejBaigaa),
    path('', include('myapi.urls')),
    path('asset/submit/', views.hyanasan),

    path('simple/choose/', views.choose),
    path('simple/firstOrThird/', views.firstOrThird),
    path('simple/form/', views.form),
    path('simple/info/', views.info),
    path('simple/company/', views.infoCompany),
    path('simple/getProducts/', views.getProducts),
    path('simple/save/', views.saveForm),
    path('simple/simpleNiitShaardah/', views.simpleNiitShaardah),
    path('simple/deleteShaardah/', views.deleteShaardah),
    path('simple/firm/', views.firm),
    path('simple/submit/', views.firmed),
    path('simple/nyarav/', views.nyarav),
    path('simple/viewShaardah/', views.viewShaardah),
    path('simple/impresion/', views.export_page),

    path('dugaarShuultChoose/', views.dugaarShuultChoose),
    path('dugaarShuult/', views.dugaarShuult),
    path('prepaid/', views.getprepix),
    path('postpaid/', views.getprepix),
    path('numberPrice/', views.numberPrice),
    path('zahialga/', views.zahialga),
    path('niitDugaarShuult/', views.niitDugaarShuult),
    path('more/', views.more),
    path('firmNumbers/', views.firmNumbers),

    # url(r'^getprefix$',views.getPrefix),
    path('getnumber/', views.getNumber),
]
