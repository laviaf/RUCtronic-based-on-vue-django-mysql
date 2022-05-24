from django.conf.urls import url
# from apps.user import views


from .views import *

from django.urls import path,re_path
from .import views


app_name = 'apps.user'
urlpatterns = [

    url(r'^login/$', LoginView.as_view(), name='login'),  # 登录
    url(r'^logout/$', LogoutView.as_view(), name='logout'),  # 退出登录
    re_path(r'^orderform/$', Orderform.as_view(), name='orderform'), #买家订单页面
    re_path(r'^orderform/$', Orderform.as_view(), name='orderform'), #买家订单页面
    re_path(r'^SalesPromotion/$', SalesPromotion.as_view(), name='SalesPromotion'),
    re_path(r'^shoppingcart/$', Shoppingcart.as_view(), name='shoppingcart'), #购物车页面
    re_path(r'^userinfoview/$', UserInfoView.as_view(), name='userinfoview'),
    re_path(r'^gettypes/$', getTypes.as_view(),name='gettypes'),
    re_path(r'^searchgoods/$',searchGoods.as_view(),name='searchgoods'),
    re_path(r'^register/$',RegisterView.as_view(),name = 'register'),
    re_path(r'^getgoodslist/$', getGoodsList.as_view(), name='getgoodslist'),
    re_path(r'^goodDetail/$', goodsDetail.as_view(), name = 'goodsDetail'),
    re_path(r'^getrecommendlist/$', getRecommendList.as_view(), name = 'getrecommendlist')
]