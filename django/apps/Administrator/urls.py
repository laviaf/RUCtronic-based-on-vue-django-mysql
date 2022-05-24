from django.conf.urls import url
# from apps.user import views


from .views import *

from django.urls import path,re_path
from .import views


app_name = 'apps.user'
urlpatterns = [
    re_path(r'^register/$', RegisterView.as_view(), name='register'),  # 注册页面
    re_path(r'^login/$', LoginView.as_view(), name='login'),  # 登录
    re_path(r'^gettopgoods/$',gettopgoods.as_view(), name='gettopgoods'),
    re_path(r'^gettopseller/$',gettopseller.as_view(), name='gettopseller'),
    re_path(r'^getaccount/$', getaccount.as_view(), name='getaccount'),
    re_path(r'^getbuytop/$',getbuytop.as_view(), name='getbuytop'),
    re_path(r'^getprovinceorder/$', getProvinceOrder.as_view(), name='getprovinceorder'),
]