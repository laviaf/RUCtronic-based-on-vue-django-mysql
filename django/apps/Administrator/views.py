import json
from django.shortcuts import render
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_decode_handler
import time
# from django.urls import path, include
# from django.conf.urls import url
# from rest_framework.routers import DefaultRouter
# from . import views

# #app_name = 'apps.Customer'
#
# urlpatterns = [
#     url('', views.CustomerView.as_view()),
#
# ]

# Create your views here.

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import connection
import mysql.connector
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import time
import datetime
from django.contrib.auth import authenticate, login, logout

from django.views.generic.base import View

# django提供了一个Paginator类帮助我们管理分页 https://blog.csdn.net/xinyan233/article/details/80236557
# 参考 https://zhuanlan.zhihu.com/p/400629292
#导入相关模块
#Paginator：分页器对象 PageNotAnlnteger：页码不是一个整数时引发该异常 EmptyPage：页码不再有效范围时引发该异常
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage



def get_User(token):
    userId = jwt_decode_handler(token)['user_id']
    user = User.objects.get(username = userId)
    return user


User = get_user_model()

class RegisterView(View):
    """注册"""

    def post(self, request):
        # 进行注册处理
        # 接收数据
        data_json = json.loads(request.body)
        code = data_json.get('code')
        username = data_json.get('username')
        password = data_json.get('password')


        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='RUCtronic',
                                       auth_plugin="mysql_native_password")
        cursor = conn.cursor()
        sql = 'SELECT Code FROM Administrator WHERE %s IN (SELECT Code FROM Administrator)'
        cursor.execute(sql, [code])
        result = cursor.fetchall()

        if result:
            if not all([username, password]):
                # 数据不完整
                return JsonResponse({'err': '数据不完整'})

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # 用户名不存在
                user = None

            if user:
                return JsonResponse({'err': '用户已存在'})

            # 进行业务处理：进行用户注册
            user = User.objects.create_user(username=username, is_type= -1)
            password = make_password(password)
            user.password = password
            user.save()

            cursor.execute(
                "INSERT INTO Administrator (AdminId,AdminPassword)"
                "values (%s,%s)",
                [username, password])
            conn.commit()
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            data = {
                'name': username,
                'token': token,
                'code': 0,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'message':'没有权限注册','code':-1})


class LoginView(View):
    """登录"""

    def get(self, request):
        # 显示登录页面
        # 判断是否记住密码
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')  # request.COOKIES['username']
            checked = 'checked'
        else:
            username = ''
            checked = ''

        return JsonResponse({'username': username, 'checked': checked})

    def post(self, request):
        # 接受数据
        data_json = json.loads(request.body)

        username = data_json.get('username')
        password = data_json.get('password')

        # remember = request.POST.get('remember')  # on

        # 校验数据
        if not all([username, password]):
            return JsonResponse({'errmsg': '数据不完整'})

        # 业务处理: 登陆校验
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                # print("User is valid, active and authenticated")
                login(request, user)  # 登录并记录用户的登录状态

                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                # 获取登录后所要跳转到的地址, 默认跳转首页
                # next_url = request.GET.get('next', reverse('goods:index'))
                #
                # #  跳转到next_url
                # response = redirect(next_url)  # HttpResponseRedirect

                # 设置cookie, 需要通过HttpReponse类的实例对象, set_cookie
                # HttpResponseRedirect JsonResponse
                next_url = request.GET.get('next', reverse('user:register'))

                #  跳转到next_url
                response = redirect(next_url)  # HttpResponseRedirect
                # 判断是否需要记住用户名
                remember = request.POST.get('remember')
                if remember == 'on':
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')
                print('hahahah')
                data = {
                    'data' :{
                                'name': username,
                                'token': token,
                             },
                    'code': 0,
                }
                print(data)
                # 回应 response
                return JsonResponse(data)

            else:
                # print("The passwoed is valid, but the account has been disabled!")
                return JsonResponse({'errmsg': '账户未激活'})
        else:
            return JsonResponse({'errmsg': '用户名或密码错误'})

class gettopgoods(View):
    def get(self, request):
        conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                       database='ructronic',
                                       auth_plugin="mysql_native_password")
        cursor = conn.cursor(dictionary=True)
        sql = 'SELECT sid,cid1,csv1 FROM (SELECT c1.SellerID sid, c1.CommodityID cid1, c2.CommodityID cid2, c1.CommoditySalesVolume csv1, c2.CommoditySalesVolume csv2 FROM commodity AS c1 LEFT JOIN commodity AS c2 ON c1.SellerID = c2.SellerID WHERE c1.CommoditySalesVolume < c2.CommoditySalesVolume) cc GROUP BY cid1 HAVING COUNT(*) <= 3 ORDER BY sid,csv1 DESC'
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:

            return JsonResponse({'data': result, 'code': 0})
        else:
            return JsonResponse({'message': 'no order'})


class gettopseller(View):
    def get(self, request):
        commodity = request.GET.get('commodity')
        commodity = str(commodity)
        conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                       database='ructronic',
                                       auth_plugin="mysql_native_password")
        cursor = conn.cursor(dictionary=True)
        sql = 'select seller.SellerID sellerid,seller.SellerName name, commodity.CommodityPrice price from commodity, seller where commodity.SellerID=seller.SellerID and CommodityName LIKE %s ORDER BY CommodityPrice limit 0,5;'
        keyword = '%' + str(commodity) + '%'
        cursor.execute(sql, [keyword])
        result = cursor.fetchall()
        if result:

            return JsonResponse({'data': result, 'code': 0})
        else:
            return JsonResponse({'message': 'no order'})

class getProvinceOrder(View):
    def get(self, request):
        conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                       database='ructronic',
                                       auth_plugin="mysql_native_password")
        cursor = conn.cursor(dictionary=True)
        sql = 'SELECT Province, ROUND(AVG(UnitPrice * Quantity),2) AverageConsumption, ROUND(MAX(UnitPrice*Quantity),2) MaximumConsumption, ROUND(MIN(UnitPrice*Quantity),2) MinimumConsumption FROM customer, orderform WHERE customer.CustomerID = orderform.CustomerID GROUP BY Province ORDER BY AVG(UnitPrice*Quantity) DESC'
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            data = {
                'data': result,
                'code': 0
            }
            print(result)
            return JsonResponse(data)
        else:
            return JsonResponse({'message': '无信息记录','code': -1})


class getaccount(View):
    def get(self, request):
        conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                       database='ructronic',
                                       auth_plugin="mysql_native_password")
        cursor = conn.cursor(dictionary=True)
        sql = 'SELECT SellerID sellerid,SellerName name,SellerIncome income FROM seller'
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            return JsonResponse({'data': result, 'code': 0})
        else:
            return JsonResponse({'message': 'no order'})

class getbuytop(View):
    def get(self, request):
        name = request.GET.get('name')
        conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                       database='ructronic',
                                       auth_plugin="mysql_native_password")
        cursor = conn.cursor(dictionary=True)

        sql = 'select * from (SELECT CustomerID, CommodityID, count(CommodityID) as volume from orderform GROUP BY CustomerID,CommodityID ORDER BY count(CommodityID) DESC ) table1  where CustomerID = %s limit 0,1'
        cursor.execute(sql, [name])
        result = cursor.fetchall()
        if result:
            return JsonResponse({'data': result, 'code': 0})
        else:
            return JsonResponse({'message': 'no order'})