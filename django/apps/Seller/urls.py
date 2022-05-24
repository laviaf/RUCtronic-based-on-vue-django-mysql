from django.conf.urls import url
# from apps.user import views


from .views import *

from django.urls import path,re_path
from .import views


app_name = 'apps.user'
urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='register'),  # 注册页面
    url(r'^login/$', LoginView.as_view(), name='login'),  # 登录
    url(r'^logout/$', LogoutView.as_view(), name='logout'),  # 退出登录
    re_path(r'^orderform/$', Orderform.as_view(), name='orderform'), #买家订单页面
    re_path(r'^shoppingcart/$', Shoppingcart.as_view(), name='shoppingcart'), #购物车页面
    re_path(r'^userinfoview/$', UserInfoView.as_view(), name='userinfoview'),
    re_path(r'^getgoodslist/$', getGoodsList.as_view(), name='getgoodslist'),
    re_path(r'^gettypes/$', getTypes.as_view(),name='gettypes'),
    re_path(r'^setgoodslist/$',setGoodsList.as_view(),name='setgoodslist'),
    re_path(r'^login/$', LoginView.as_view(), name='login'),  # 登录
    re_path(r'^updategoodslist/$',updateGoodsList.as_view(),name = 'updategoodslist'),
    re_path(r'^deletegoods/$',deleteGoods.as_view(),name = 'deletegoods'),
    re_path(r'^addgoods/$',addGoods.as_view(), name = 'addgoods'),
    re_path(r'^SalesPromotion/$',Seller_SalesPromotion.as_view(), name = 'SalesPromotion'),
    re_path(r'^getgoodslist/$', getGoodsList.as_view(), name='getgoodslist'),
    re_path(r'^getsellershopdata/$', getSellerShopData.as_view(), name='getsellershopdata'),
]