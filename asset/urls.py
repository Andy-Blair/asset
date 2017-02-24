# _*_ coding:utf-8 _*_
"""yytx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView
import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url="/asset/index/")),
    url(r'^login/$', views.login_view),
    url(r'^logout/$', views.logout_view),
    url(r'^index/$', views.index),
    url(r'^index/dataimport/$', views.dataimport),
    url(r'^index/dataexport/$', views.dataexport),
    url(r'^add/$', views.add),
    url(r'^copyadd/(\d+)$', views.copyadd),
    url(r'^modify/(\d+)', views.modify),
    url(r'^discardasset/(\d+)', views.discard),
    url(r'^discard/$', views.discard_index, name="discard_index"),  # 报废页
    url(r'^index/indexdata/', views.indexdata),  # bootstrap
    url(r'^index/discarddata/', views.discarddata),  # 报废
    url(r'^index/statistical/', views.statistical),  # 统计

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
