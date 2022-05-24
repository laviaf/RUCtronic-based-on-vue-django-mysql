"""ourproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.static import serve

from django.conf.urls import url, include
# from django.contrib import admin
from django.views.static import serve

from django.views.generic.base import TemplateView


urlpatterns = [

    path('admin/', admin.site.urls),

    #url(r'^', include(router.urls)),

    # url(r'good/$', GoodsListView.as_view(), name="goods-list"),
    path('user/', include('Customer.urls', namespace='user')),
    path('seller/', include('Seller.urls', namespace='seller')),
    path('administrator/',include('Administrator.urls', namespace='administrator')),
    #url(r'', TemplateView.as_view(template_name= 'index.html')),
]
