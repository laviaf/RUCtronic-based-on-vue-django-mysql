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



class sellerDetail(View):
    def get(self, request):
        seller_id = request.GET.get('seller_id')
        try:
            page = request.GET.get('page')
        except:
            page = 0

        conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                       database='RUCtronic',
                                       auth_plugin="mysql_native_password")
        cursor = conn.cursor()
        if page == 0 or page is None:
            sql = 'SELECT * FROM Seller WHERE SellerID = %s'
            cursor.execute(sql, [seller_id])
            result = cursor.fetchall()

            return JsonResponse(result, safe=False)
        else:
            # sql = "SELECT OrderID,OrderState,OrderExpress,OrderDate,CommodityName FROM Orderform o, Commodity c WHERE o.CommodityID = c.CommodityID AND o.CustomerID = %s"
            sql = "SELECT * FROM Commodity c WHERE c.SellerID = %s"
            cursor.execute(sql, [seller_id])
            '''逐行读取行，若没有数据返回为空'''
            result = cursor.fetchall()
            if result:
                paginator = Paginator(result, int(len(result) / 10 + 1))  # 生成Paginator对象
                page_number = page  # 获取当前页数
                try:
                    commodity = paginator.get_page(page_number)  # 返回page_number对应的索引对象
                except PageNotAnInteger:  # 如果页码非数字，返回第一页
                    commodity = paginator.get_page(1)
                except EmptyPage:
                    if request.is_ajax():  # 判断网页是否以ajax形式交互，如果是返回空值
                        return HttpResponse('')
                    commodity = paginator.page(paginator.num_pages)  # 否则返回最后一页内容
                # 判断网页是否以ajax形式交互，如果是，进行增量更新
                if request.is_ajax():
                    #return render(request, 'orderform.html', {'order': order})
                    return JsonResponse({'commodity': list(commodity)})
                # 当前页面信息
                # data = {}
                # for i in range(len(result)):
                #     string = 'commodity' + str(i + 1)
                #     data[string] = str(result[i])
                commodity_count = len(commodity)
                data = {
                    'commodity': list(commodity),
                    'commodity_count': commodity_count,
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'message': 'no order', 'code': -1})

class UserInfoView(View):
    """购物车显示"""
    def get(self, request):
        token = request.GET.get('token')
        user = get_User(token)
        sellerId = user.username
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='RUCtronic',
                                       auth_plugin="mysql_native_password")

        cursor = conn.cursor(dictionary=True)
        sql = "SELECT SellerId Id,SellerName Name,SellerProfilePhoto Img,SellerLV Lv,SellerAddress Address,SellerIncome Income,SellerTELE TELE FROM seller WHERE SellerId = %s"
        cursor.execute(sql, [sellerId])
        info = cursor.fetchall()
        if info:
            info = info[0]
            LV = ['青铜','黄金','钻石','王者']
            info['Lv'] = LV[int(info['Lv'])]
            data = {
                'data': info,
                'code': 0
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'message': '无用户信息', 'code': -1})


    def post(self, request):
        data_json = json.loads(request.body)
        token = data_json.get('token')
        operation = data_json.get('operation')
        user = get_User(token)
        sellerId = user.username
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='RUCtronic',
                                       auth_plugin="mysql_native_password")

        cursor = conn.cursor(dictionary=True)
        if operation == 1:
            Name = data_json.get('nickname')
            Address = data_json.get('address')
            TELE = data_json.get('phone')

            sql = 'UPDATE seller SET SellerName = %s, SellerAddress = %s, SellerTELE = %s WHERE SellerID = %s'
            cursor.execute(sql, [Name, Address, TELE, sellerId])
            conn.commit()
            return JsonResponse({'code': 0})
        else:
            data_json = json.loads(request.body)
            newPwd = data_json.get('newPwd')
            user = User.objects.get(username=sellerId)
            newPwd = make_password(newPwd)
            user.set_password(newPwd)
            user.save()

            sql = 'UPDATE seller SET SellerPassword = %s WHERE SellerID = %s'
            cursor.execute(sql, [newPwd, sellerId])
            conn.commit()
            return JsonResponse({'code': 0})

class setGoodsList(View):
    def get(self,request):
        token = request.GET.get('token')
        user = get_User(token)
        sellerId = user.username
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='RUCtronic',
                                       auth_plugin="mysql_native_password")

        cursor = conn.cursor(dictionary=True)
        sql = 'SELECT CommodityID id,CommodityName name,CommodityProfilePhoto img,Commodity_description spec,CommodityInventory goodsNum,CommodityOriginalPrice original,CommodityPrice unitprice,CommodityType type,Maxbuy maxbuy,SalesPromotionID promotion FROM commodity WHERE SellerID = %s'
        cursor.execute(sql,[sellerId])
        result = cursor.fetchall()
        if result:
            for i in range(len(result)):
                result[i]['temGoodsNum'] = 0
            data = {'data':result,
                    'code':0}
            return JsonResponse(data)
        else:
            return JsonResponse({'message':'不存在商品', 'code': -1})

class updateGoodsList(View):
    def post(self,request):
        data_json = json.loads(request.body)
        token = data_json.get('token')
        user = get_User(token)
        sellerId = user.username
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='RUCtronic',
                                       auth_plugin="mysql_native_password")
        print(sellerId)
        cursor = conn.cursor(dictionary=True)
        goodsid = data_json.get('goodsId')
        goodsname = data_json.get('name')
        goodsimg = data_json.get('img')
        goodsspec = data_json.get('spec')
        goodsoriginal = data_json.get('original')
        goodsunit = data_json.get('unitprice')
        goodstype = data_json.get('type')
        goodsnum = data_json.get('goodsnum')
        goodsmaxbuy = data_json.get('maxbuy')
        promotion = data_json.get('promotion')
        sql = 'UPDATE commodity SET CommodityName = %s,CommodityProfilePhoto = %s,Commodity_description = %s,CommodityInventory = %s,CommodityOriginalPrice = %s,CommodityPrice = %s,CommodityType = %s,Maxbuy = %s, SalesPromotionID = %s WHERE SellerID = %s AND CommodityID = %s'
        cursor.execute(sql, [goodsname, goodsimg, goodsspec, goodsnum, goodsoriginal, goodsunit, goodstype, goodsmaxbuy,promotion,sellerId, goodsid])
        conn.commit()
        return JsonResponse({'code': 0})

class deleteGoods(View):
    def post(self,request):
        data_json = json.loads(request.body)
        token = data_json.get('token')
        user = get_User(token)
        sellerId = user.username
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='RUCtronic',
                                       auth_plugin="mysql_native_password")

        cursor = conn.cursor(dictionary=True)

        goodsid = data_json.get('goodsId')

        sql = 'DELETE FROM commodity WHERE SellerID = %s AND CommodityID = %s'
        cursor.execute(sql, [sellerId, goodsid])
        conn.commit()
        return JsonResponse({'code': 0})

class addGoods(View):
    def post(self,request):
        data_json = json.loads(request.body)
        token = data_json.get('token')
        user = get_User(token)
        sellerId = user.username
        goodsname = data_json.get('name')
        goodsimg = data_json.get('img')
        goodsspec = data_json.get('spec')
        goodsoriginal = data_json.get('original')
        goodsunit = data_json.get('unitprice')
        goodstype = data_json.get('type')
        goodsnum = data_json.get('num')
        goodsmaxbuy = data_json.get('maxbuy')
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='RUCtronic',
                                       auth_plugin="mysql_native_password")

        cursor = conn.cursor(dictionary=True)

        present_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        goodsid = sellerId + present_time

        sql = 'INSERT INTO commodity(CommodityID,CommodityName,CommodityProfilePhoto,SellerID,Commodity_description,CommodityOriginalPrice,CommodityPrice,CommodityInventory,CommodityType,Maxbuy) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, [goodsid, goodsname, goodsimg, sellerId, goodsspec, goodsoriginal, goodsunit, goodsnum, goodstype,goodsmaxbuy])
        conn.commit()
        sql = 'SELECT CommodityID FROM commodity WHERE CommodityID = %s AND CommodityProfilePhoto IS NULL'
        cursor.execute(sql, [goodsid])
        result = cursor.fetchall()
        if result:
            return JsonResponse({'code': 0})
        else:
            sql = 'UPDATE commodity SET CommodityProfilePhoto = %s WHERE CommodityID = %s'
            img = 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fc-ssl.duitang.com%2Fuploads%2Fitem%2F201506%2F22%2F20150622103608_djBM8.thumb.400_0.jpeg&refer=http%3A%2F%2Fc-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1643382591&t=1a4ab4a22269ec71c32ba80944f5de3a'
            cursor.execute(sql, [img, goodsid])
            conn.commit()
            return JsonResponse({'code': 0})


class getSellerShopData(View):
    def get(self,request):
        sellerId = request.GET.get('id')
        print(sellerId)
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='RUCtronic',
                                       auth_plugin="mysql_native_password")

        cursor = conn.cursor(dictionary=True)
        sql = 'SELECT CommodityID id,CommodityName name, Commodity_description spec, CommodityProfilePhoto img, CommodityPrice unitprice, CommoditySalesVolume volume FROM commodity WHERE SellerID = %s'
        cursor.execute(sql, [sellerId])
        result = cursor.fetchall()
        if result:
            data = {
                'data':result,
                'code': 0
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'message':'不存在商品', 'code': -1})

class getGoodsList(View):
    def get(self,request):
        typeId = request.GET.get('typeId')
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='RUCtronic',
                                       auth_plugin="mysql_native_password")

        cursor = conn.cursor(dictionary=True)
        sql = 'SELECT CommodityID id, CommodityProfilePhoto img, CommodityName name, CommodityPrice price FROM commodity WHERE CommodityType = %s'
        cursor.execute(sql, [typeId])
        result = cursor.fetchall()
        if result:
            data = {'data': result,
                    'code': 0}
            return JsonResponse(data)
        else:
            return JsonResponse({'message':'无该种类商品', 'code': -1})

class getTypes(View):
    def get(self,request):
        print('hahahah')
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='RUCtronic',
                                       auth_plugin="mysql_native_password")

        cursor = conn.cursor(dictionary=True)
        sql = 'SELECT DISTINCT CommodityType FROM commodity GROUP BY CommodityType'
        cursor.execute(sql)
        result = cursor.fetchall()

        if result:
            data = {'data': result,
                    'code': 0}
            return JsonResponse(data)
        else:
            return JsonResponse({'message':'无该种类', 'code': -1})

# class CustomerView(ListCreateAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerDetailsSerializer


class RegisterView(View):
    """注册"""

    def post(self, request):
        # 进行注册处理
        # 接收数据
        data_json = json.loads(request.body)
        nickname = data_json.get('nickname')
        username = data_json.get('username')
        password = data_json.get('password')
        address = data_json.get('address')
        phone = data_json.get('phone')
        # 初始头像
        img = 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Finews.gtimg.com%2Fnewsapp_bt%2F0%2F8755112998%2F640&refer=http%3A%2F%2Finews.gtimg.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1643464126&t=e50918f1af8ede9eef34c8724ed0db09'
        is_type = data_json.get('is_type')

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
        user = User.objects.create_user(username=username, is_type=is_type)
        password = make_password(password)
        user.password = password
        user.save()


        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='RUCtronic',
                                       auth_plugin="mysql_native_password")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO seller (Sellerid,SellerName,SellerPassword, SellerLv, SellerTELE, SellerAddress, SellerProfilePhoto, SellerIncome)"
                           "values (%s,%s,%s,%s,%s,%s,%s,%s)", [username,nickname, password, 0, phone, address, img, 0])
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


# /user/logout
class LogoutView(View):
    """退出登录"""

    def get(self, request):
        logout(request)

        return JsonResponse({})




class Orderform(View):
    '''订单状态页面'''

    def get(self, request):

        token = request.GET.get('token')
        user = get_User(token)
        is_type = user.is_type  # 登录该页面的用户性质
        is_type = int(is_type)  # 将字符串转成int类型

        if is_type == 1:  # 如果是卖家
            state = int(request.GET.get('state'))
            seller_id = user.username

            # 连接数据库
            '''获取订单ID、订单状态、快递单号、订单日期、商品名称'''
            conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                           database='ructronic',
                                           auth_plugin="mysql_native_password")
            cursor = conn.cursor(dictionary=True)

            if state == -1:
                sql = "SELECT o.OrderID id,o.OrderDate createtime,o.OrderState state,c.CommodityProfilePhoto img,c.Commodity_description spec,c.CommodityID com_id,c.CommodityName com_name,c.CommodityPrice unitPrice,o.Quantity num,o.Quantity*o.UnitPrice amount,o.IsRating FROM Orderform o, Commodity c WHERE o.CommodityID = c.CommodityID AND o.SellerID = %s"
                cursor.execute(sql, [seller_id])
                '''逐行读取行，若没有数据返回为空'''
                result = cursor.fetchall()
            else:
                sql = "SELECT o.OrderID id,o.OrderDate createtime,o.OrderState state,c.CommodityProfilePhoto img,c.Commodity_description spec,c.CommodityID com_id,c.CommodityName com_name,c.CommodityPrice unitPrice,o.Quantity num,o.Quantity*o.UnitPrice amount,o.IsRating FROM Orderform o, Commodity c WHERE o.CommodityID = c.CommodityID AND o.SellerID = %s AND o.OrderState = %s"
                cursor.execute(sql, [seller_id, state])
                '''逐行读取行，若没有数据返回为空'''
                result = cursor.fetchall()

            if result:
                paginator = Paginator(result, int(len(result) / 10 + 1))  # 生成Paginator对象
                page_number = request.GET.get('page')  # 获取当前页数
                try:
                    order = paginator.get_page(page_number)  # 返回page_number对应的索引对象
                except PageNotAnInteger:  # 如果页码非数字，返回第一页
                    order = paginator.get_page(1)
                except EmptyPage:
                    if request.is_ajax():  # 判断网页是否以ajax形式交互，如果是返回空值
                        return HttpResponse('')
                    order = paginator.page(paginator.num_pages)  # 否则返回最后一页内容
                # 判断网页是否以ajax形式交互，如果是，进行增量更新
                if request.is_ajax():
                    # return render(request, 'orderform.html', {'order': order})
                    return JsonResponse({'order': list(order)})

                return JsonResponse({'data': result, 'code': 0})
            else:
                return JsonResponse({'message': 'no order', 'code':-1})
            conn.close()
        else:
            return JsonResponse({'message': 'with no option', 'code': -1})

    ''''当买家或卖家作出修改请求时'''

    def post(self, request):
        data_json = json.loads(request.body)

        token = data_json.get('token')
        user = get_User(token)
        is_type = user.is_type  # 登录该页面的用户性质

        is_type = int(is_type)  # 将字符串转成int类型
        if is_type == 1:  # 卖家
            cus_update = int(data_json.get('modify_type'))
            # 连接数据库
            conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                           database='ructronic',
                                           auth_plugin="mysql_native_password")
            cursor = conn.cursor(dictionary=True)

            # cus_update： 2：发货  4：作废
            if cus_update == 2:
                orderId = data_json.get('orderId')
                OrderExpressNO = data_json.get('expressNo')

                sql = 'UPDATE Orderform SET OrderState = %s, OrderExpressNO = %s WHERE OrderID = %s'
                cursor.execute(sql, [1, OrderExpressNO, orderId])
                conn.commit()

                return JsonResponse({'code': 0})
            elif cus_update == 4:
                orderId = data_json.get('orderId')

                sql = 'UPDATE Orderform SET OrderState = %s WHERE OrderID = %s'
                cursor.execute(sql, [3, orderId])
                conn.commit()

                return JsonResponse({'code': 0})
            else:  # 其他操作不被允许
                return JsonResponse({'update': 'No permission', 'code': -1})
            conn.close()

        else:
            return JsonResponse({'message': 'with no option', 'code': -1})

class Shoppingcart(View):
    # 购物车页面
    def get(self, request):

        token = request.GET.get('token')
        user = get_User(token)
        cus_id = user.username
        now_time = time.strftime("%Y-%m-%d", time.localtime())
        # 连接数据库
        conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                       database='RUCtronic',
                                       auth_plugin="mysql_native_password")
        cursor = conn.cursor(dictionary=True)
        '''商品名称、商品数量'''

        sql = 'SELECT c.CommodityID id,c.CommodityName name, c.CommodityPrice unitPrice,c.Commodity_description spec,s.CommodityQuantity goodsNum,c.CommodityProfilePhoto img,c.Maxbuy maxBuy FROM Commodity c,Shoppingcart s WHERE c.CommodityID = s.CommodityID AND s.CustomerID = %s'
        cursor.execute(sql, [cus_id])
        result = cursor.fetchall()

        sql = 'SELECT s.discount FROM salespromotion s,Commodity c,Shoppingcart sh WHERE s.SalesPromotionID = c.SalesPromotionID AND c.CommodityID = sh.CommodityID AND sh.CustomerID = %s AND %s>=s.startdate AND %s<=s.enddate'
        cursor.execute(sql, [cus_id, now_time, now_time])
        time_result = cursor.fetchall()
        if result:
            paginator = Paginator(result, int(len(result) / 10 + 1))  # 生成Paginator对象
            page_number = request.GET.get('page')  # 获取当前页数
            try:
                cart = paginator.get_page(page_number)  # 返回page_number对应的索引对象
            except PageNotAnInteger:  # 如果页码非数字，返回第一页
                cart = paginator.get_page(1)
            except EmptyPage:
                if request.is_ajax():  # 判断网页是否以ajax形式交互，如果是返回空值
                    return HttpResponse('')
                cart = paginator.page(paginator.num_pages)  # 否则返回最后一页内容
            # 判断网页是否以ajax形式交互，如果是，进行增量更新
            if request.is_ajax():
                # return render(request, 'orderform.html', {'shoppingcart': cart})
                return JsonResponse({'shoppingcart': list(cart)})
            # 当前页面信息
            conn.close()
            data = []
            for i in range(len(result)):
                result[i]['temGoodsNum'] = 0
                result[i]['amount'] = 0
                if time_result[i]:
                    result[i]['discount'] = time_result[i]['discount']
                else:
                    result[i]['discount'] = 1.0
                data.append(result[i])

            data = {
                'data': data,
                'code': 0
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'message': 'no order', 'code': -1})

    def post(self, request):
        # 买家作出请求
        #cus_id = request.POST.get('cus_id') #获取买家ID
        token = request.GET.get('token')
        user = get_User(token)
        cus_id = user.username

        data_json = json.loads(request.body)
        update = data_json.get('cus_update')
        update = int(update)     #修改商品的操作 0：删除商品数量，1：购买商品
        if update == 0: #删除商品数量
            com_id = data_json.get('orderId')
            conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                           database='RUCtronic',
                                           auth_plugin="mysql_native_password")
            cursor = conn.cursor(dictionary=True)

            sql = 'DELETE FROM shoppingcart s WHERE CustomerID = %s AND CommodityID = %s'
            cursor.execute(sql,[cus_id, com_id])
            conn.commit()
            conn.close()
            return JsonResponse({'code':0})
        else:#购买商品
            cartList = data_json.get('cartList')
            conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                           database='RUCtronic',
                                           auth_plugin="mysql_native_password")
            cursor = conn.cursor(dictionary=True)
            for i in range(len(cartList)):
                com_id = cartList[i]['orderId']
                com_num =cartList[i]['goodsNum']
                unitPrice = cartList[i]['unitPrice']
                unitPrice = float(unitPrice)
                amount = cartList[i]['amount']
                amount = float(amount)
                sql = 'SELECT CommodityInventory inventory FROM commodity WHERE CommodityID = %s'
                cursor.execute(sql, [com_id])
                inventory = cursor.fetchall()
                print(inventory)
                inventory = int(inventory[0]['inventory'])
                if com_num > inventory:
                    return JsonResponse({'message': '库存不足', 'code': -1})
                else:
                    sql = 'SELECT CustomerBalance balance FROM customer WHERE CustomerID = %s'
                    cursor.execute(sql, [cus_id])

                    balance = cursor.fetchall()
                    balance = float(balance[0]['balance'])
                    if balance < amount:
                        return JsonResponse({'message': '账户余额不足，支付失败', 'code': -1})
                    else:
                        sql = 'UPDATE commodity SET CommodityInventory = CommodityInventory - %s WHERE CommodityID = %s'
                        cursor.execute(sql, [com_num, com_id])
                        conn.commit()
                        sql = 'UPDATE customer SET CustomerBalance = Cu stomerBalance - %s WHERE CustomerID = %s'
                        cursor.execute(sql, [amount, cus_id])
                        conn.commit()
                        sql = 'SELECT c.SellerID sel_id FROM commodity c,shoppingcart s WHERE s.CustomerID = %s AND s.CommodityID = %s AND s.CommodityID = c.CommodityID'
                        cursor.execute(sql, [cus_id, com_id])
                        sel_id = cursor.fetchall()
                        sel_id = sel_id[0]['sel_id']
                        now_time = time.strftime("%Y-%m-%d", time.localtime())
                        present_time = time.strptime('%Y%m%d%H%M%S',time.localtime())
                        orderid = com_id+cus_id+present_time
                        sql = 'INSERT INTO orderform(OrderID,SellerID,CommodityID,CustomerID,Quantity,UnitPrice,OrderDate,OrderState) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
                        cursor.execute(sql, [orderid, sel_id, com_id, cus_id, com_num, unitPrice, now_time, 0])
                        conn.commit()
                        sql = 'DELETE FROM shoppingcart WHERE CustomerID = %s AND CommodityID = %s'
                        cursor.execute(sql, [cus_id, com_id])
                        conn.commit()
                        conn.close()
                        return JsonResponse({'code': 0})






'''
定义数据获取函数
'''

#买家查看已完成订单的评价
def customer_get_comments(Customerid, cursor):
    sql = 'SELECT o.OrderID, o.CommodityID, c.CommodityName, o.Quantity, o.UnitPrice, o.OrderDate, p.Comment, p.Rating FROM Purchased p, Orderform o, Commodity c WHERE o.CustomerID = %s and o.CommodityID  = c.CommodityID and p.OrderID = o.OrderID'
    cursor.execute(sql, [Customerid])
    data = cursor.fetchall()

    return data

#买家进行评价修改
def customer_modify_comments(comment, rating, SuccessFormID, cursor, conn):
    sql = 'UPDATE Purchased SET Comment = %s, Rating = %s WHERE SuccessFormID = %s'
    cursor.execute(sql, [comment, rating, SuccessFormID])
    conn.commit()

#卖家查看订单
'''
note：这里返回的订单顺序是按照完成状态+时间顺序返回的，但问题是如何按照待发货、已发货、已完成、作废顺序排序？
'''
def seller_get_orders(Sellerid, cursor):
    sql = 'SELECT o.OrderID, o.CommodityID, c.CommodityName, o.Quantity, o.OrderDate, o.OrderState FROM Orderform o, Commodity c WHERE o.SellerID = %s and o.CommodityID = c.CommodityID ORDER BY o.OrderState, o.OrderDate'
    cursor.execute(sql, [Sellerid])
    data = cursor.fetchall()

    return data

#卖家取消订单
def seller_delete_orders(Orderid, cursor, conn):
    sql = 'UPDATE Orderform SET OrderState = \'作废\' WHERE OrderID = %s'
    cursor.execute(sql, [Orderid])
    conn.commit()

#卖家发货
def seller_modify_orders(express_no, Orderid, cursor ,conn):
    sql = 'UPDATE Orderform SET OrderState = \'已发货\', OrderExpressNO = %s WHERE OrderID = %s'
    cursor.execute(sql, [express_no,Orderid])
    conn.commit()

#查看卖家自己的促销活动
def seller_get_SalesPromotion(Sellerid, cursor):
    sql = 'SELECT SalesPromotionID, SalesPromotionName, startdate, enddate, SalesPromotion_description FROM SalesPromotion sp WHERE sp.SellerID = %s'
    cursor.execute(sql, [Sellerid])
    data = cursor.fetchall()

    return data

#卖家删除活动
def seller_delete_SalesPromotion(SalesPromotionID,cursor,conn):
    sql = 'DELETE FROM SalesPromotion WHERE SalesPromotionID = %s'
    cursor.execute(sql, [SalesPromotionID])
    conn.commit()

#卖家修改活动
def seller_modify_SalesPromotion(SalesPromotionID, discount_scale, cursor, conn):
    sql = 'UPDATE SalesPromotion SET discount_scale = %s WHERE SalesPromotionID = %s'
    cursor.execute(sql, [discount_scale,SalesPromotionID])
    conn.commit()

#卖家添加活动
def seller_add_SalesPromotion(SalesPromotionid,SalesPromotionName,SellerID,startdate,discount_scale,cursor,conn):
    sql = 'INSERT INTO SalesPromotion(SalesPromotionid,SalesPromotionName,SellerID,startdate,discount_scale) VALUES (%s,%s,%s,%s,%s)'
    cursor.execute(sql, [SalesPromotionid,SalesPromotionName,SellerID,startdate,discount_scale])
    conn.commit()

'''
note：
1. 统一考虑界面跳转问题
2. 多参数execute问题:%s是否匹配其他数据格式

3.订单签收后需自动增加Evalueate记录

4. 需要添加查找功能
5. 数据修改之后界面刷新？ 
6. SalesPromotion_description变量需要修改
7. 修改不成功返回的信息
8. 卖家对于订单进行作废是否需要增加只有未发货才能作废？
'''
#分页
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#买家对已购买订单的评论进行操作
class Customer_Comments(View):
    def get(self, request):
        page = request.GET.get('page')
        #先判断买家是否登录
        user = request.user
        is_type = user.is_type
        is_type = int(is_type)

        #确认为买家
        if is_type == 0:
            #连接数据库
            conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                           database='RUCtronic',
                                           auth_plugin="mysql_native_password")
            cursor = conn.cursor()

            Customerid = user.username
            result = customer_get_comments(Customerid, cursor)

            if result:
                paginator = Paginator(result, int(len(result)/10)+1)   #生成Paginator对象
                page_number = page    #获取当前页数

                #ajax：网页增量更新交互方式
                try:
                    comments = paginator.get_page(page_number)    #返回page_number对应的索引对象，同时处理异常页码
                except PageNotAnInteger:        #如果页码非数字，返回第一页
                    comments = paginator.get_page(1)    #返回Page对象
                except EmptyPage:               #如果为空
                    if request.is_ajax():       #判断网页是否以ajax形式交互，如果是
                        return HttpResponse('') #返回空值
                    comments = paginator.get_page(paginator.num_pages)  #否则返回最后一页内容

                #判断网页是否以ajax形式交互，如果是，进行增量更新
                if request.is_ajax():
                    return JsonResponse({'comments': comments})

                #如果不是ajax交互，返回网页框架
                #当前页面信息
                main_top_info = '订单列表'
                #历史评价总数
                comments_count = len(result)
                data = {
                    'comments': list(comments),
                    'comments_count': comments_count,
                    'main_top_info': main_top_info
                }
                return JsonResponse(data)

            else:
                return JsonResponse('No history comments.', safe=False)

        else:
            return JsonResponse({'errmsg': '非法定买家！请重新登录'})

    def post(self, request):
        #先判断买家是否登录
        user = request.user
        is_type = user.is_type
        is_type = int(is_type)

        #确认为买家
        if is_type == 0:
            #连接数据库
            conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                           database='RUCtronic',
                                           auth_plugin="mysql_native_password")
            cursor = conn.cursor()

            #对已购买商品的评论进行修改
            Orderid = request.POST.get('OrderID')
            rating = request.POST.get('Rating')
            comment = request.POST.get('Comment')

            sql = 'UPDATE Purchased SET Comment = %s, Rating = %s WHERE SuccessFormID = %s'
            cursor.execute(sql, [comment, rating, SuccessFormID])
            conn.commit()
            conn.close()
            return JsonResponse({})

        else:
            return JsonResponse({'errmsg': '非法定买家！请重新登录'})

#卖家对订单进行操作
class Seller_Order(View):
    def get(self, request):
        #先判断买家是否登录
        user = request.user
        is_type = user.is_type
        is_type = int(is_type)

        page = request.GET.get('page')
        #确认为卖家
        if is_type == 1:
            #连接数据库
            conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                           database='RUCtronic',
                                           auth_plugin="mysql_native_password")
            cursor = conn.cursor()

            Sellerid = user.username
            # result = seller_get_orders(Sellerid, cursor)
            sql = 'SELECT o.OrderID, o.CommodityID, c.CommodityName, o.Quantity, o.OrderDate, o.OrderState FROM Orderform o, Commodity c WHERE o.SellerID = %s and o.CommodityID = c.CommodityID ORDER BY o.OrderState, o.OrderDate'
            cursor.execute(sql, [Sellerid])
            result = cursor.fetchall()

            if result:
                paginator = Paginator(result, int(len(result)/10)+1)   #生成Paginator对象
                page_number = request.GET.get('page')    #获取当前页数

                #ajax：网页增量更新交互方式
                try:
                    orders = paginator.get_page(page_number)    #返回page_number对应的索引对象，同时处理异常页码
                except PageNotAnInteger:        #如果页码非数字，返回第一页
                    orders = paginator.get_page(1)    #返回Page对象
                except EmptyPage:               #如果为空
                    if request.is_ajax():       #判断网页是否以ajax形式交互，如果是
                        return HttpResponse('') #返回空值
                    orders = paginator.get_page(paginator.num_pages)  #否则返回最后一页内容

                #判断网页是否以ajax形式交互，如果是，进行增量更新
                if request.is_ajax():
                    return  JsonResponse({'orders': list(orders)})
                    #return render(request, 'orders.html', {'orders': orders})

                #如果不是ajax交互，返回网页框架
                #当前页面信息
                main_top_info = '订单列表'
                #促销活动总数
                orders_count = len(result)
                return JsonResponse({
                    'orders': list(orders),
                    'orders_count': orders_count,
                    'main_top_info': main_top_info})
                # return render(request, 'orders.html', {
                #     'orders': orders,
                #     'orders_count': orders_count,
                #     'main_top_info': main_top_info
                # })

            else:
                return JsonResponse('No history orders.')

        else:
            return JsonResponse({'errmsg': '非法定卖家！请重新登录'})

    def post(self, request):
        #先判断买家是否登录
        user = request.user
        is_type = user.is_type
        is_type = int(is_type)

        #确认为卖家
        if is_type == 1:
            #连接数据库
            conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                           database='RUCtronic',
                                           auth_plugin="mysql_native_password")
            cursor = conn.cursor()

            #对需要作出修改的类型进行判断
            modify_type = int(request.POST.get('modify_type'))
            '''
            note：这里需要返回修改类型  若为1，则发货，若为0，则取消订单
            note：若发货，需要返回买家选定的订单id+快递单号
            '''
            if modify_type == 0:
                Orderid = request.POST.get('OrderID')
                sql = 'SELECT o.OrderState FROM Orderform o WHERE o.OrderID = %s'
                cursor.execute(sql, [Orderid])
                state = cursor.fetchone()
                if state[0] != '待发货':
                    return JsonResponse({'errmsg': '当前订单不可作废'})
                else:
                    # seller_delete_orders(Orderid, cursor)
                    sql = 'UPDATE Orderform SET OrderState = \'作废\' WHERE OrderID = %s'
                    cursor.execute(sql, [Orderid])
                    conn.commit()
                    return  JsonResponse({})

            elif modify_type == 1:
                Orderid = request.POST.get('OrderID')
                express_no = request.POST.get('OrderExpressNO')
                sql = 'SELECT o.OrderState FROM Orderform o WHERE o.OrderID = %s'
                cursor.execute(sql,[Orderid])
                state = cursor.fetchone()
                if state[0] != '待发货':
                    return JsonResponse({'errmsg': '当前订单不可修改'})
                else:
                    # seller_modify_orders(express_no, Orderid, cursor)
                    sql = 'UPDATE Orderform SET OrderState = \'已发货\', OrderExpressNO = %s WHERE OrderID = %s'
                    cursor.execute(sql, [express_no, Orderid])
                    conn.commit()
                    return JsonResponse({})


            else:
                return JsonResponse({'errmsg': '非法请求'})

        else:
            return JsonResponse({'errmsg': '非法定买家！请重新登录'})

import time
import datetime

class Seller_SalesPromotion(View):
    def get(self, request):
        token = request.GET.get('token')
        user = get_User(token)
        is_type = user.is_type
        is_type = int(is_type)

        #确认为卖家
        if is_type == 1:
            #连接数据库
            conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                           database='RUCtronic',
                                           auth_plugin="mysql_native_password")
            cursor = conn.cursor(dictionary=True)

            Sellerid = user.username
            # result = seller_get_SalesPromotion(Sellerid, cursor)
            sql = 'SELECT SalesPromotionID, SalesPromotionName, startdate, enddate, discount FROM SalesPromotion sp WHERE sp.SellerID = %s'
            cursor.execute(sql, [Sellerid])
            result = cursor.fetchall()

            if result:
                paginator = Paginator(result, int(len(result)/10)+1)   #生成Paginator对象
                page_number = request.GET.get('page')    #获取当前页数

                #ajax：网页增量更新交互方式
                try:
                    promotions = paginator.get_page(page_number)    #返回page_number对应的索引对象，同时处理异常页码
                except PageNotAnInteger:        #如果页码非数字，返回第一页
                    promotions = paginator.get_page(1)    #返回Page对象
                except EmptyPage:               #如果为空
                    if request.is_ajax():       #判断网页是否以ajax形式交互，如果是
                        return HttpResponse('') #返回空值
                    promotions = paginator.get_page(paginator.num_pages)  #否则返回最后一页内容

                #判断网页是否以ajax形式交互，如果是，进行增量更新
                if request.is_ajax():
                    # return render(request, 'promotions.html', {'promotions': promotions})
                    return JsonResponse({'promotions': list(promotions)})

                #如果不是ajax交互，返回网页框架
                #促销活动总数
                promotions_count = len(result)
                # return render(request, 'promotions.html', {
                #     'comments': promotions,
                #     'promotions_count': promotions_count,
                #     'main_top_info': main_top_info
                # })
                return JsonResponse({
                    'data':result,
                    'code':0,
                })


            else:
                return JsonResponse({'data':[],'code':0})

        else:
            return JsonResponse({'errmsg': '非法定卖家！请重新登录','code':-1})

    def post(self, request):
        #先判断买家是否登录
        data_json = json.loads(request.body)

        token = data_json.get('token')
        user = get_User(token)
        is_type = user.is_type
        is_type = int(is_type)

        #确认为卖家
        if is_type == 1:
            #连接数据库
            conn = mysql.connector.connect(host='localhost', user='root', password='root',
                                           database='RUCtronic',
                                           auth_plugin="mysql_native_password")
            cursor = conn.cursor()

            #对需要作出修改的类型进行判断
            modify_type = int(data_json.get('modify_type'))
            '''
            note：这里需要返回修改类型    若为0，则增加促销活动，若为1，则修改活动，若为2，则删除活动（只允许删除已经结束的活动）
            '''
            if modify_type == 0:
                SalesPromotionName = data_json.get('PromotionName')
                startdate = data_json.get('startTime')
                startdate = time.strptime(startdate, '%Y-%m-%d')
                enddate = data_json.get('endTime')
                enddate = time.strptime(enddate, '%Y-%m-%d')
                discount_scale = float(data_json.get('discount'))


                present_time =time.strptime(datetime.datetime.now().strftime('%Y-%m-%d'),'%Y-%m-%d')
                max_time = time.strptime('2099-12-31', '%Y-%m-%d')



                #进行修改信息判断
                if startdate > enddate:
                    return JsonResponse({'errmsg': '非法信息！起始时间需早于结束时间','code':-1})
                elif present_time > startdate:
                    return JsonResponse({'errmsg': '非法信息！开始时间需在当前时间之后','code':-1})
                elif enddate > max_time:
                    return JsonResponse({'errmsg': '非法信息！结束时间需在2099-12-31以前','code':-1})
                elif discount_scale < 0 or discount_scale > 1:
                    return JsonResponse({'errmsg': '非法信息！折扣需在0-1之间','code':-1})
                else:
                    sql = 'SELECT COUNT(*) FROM SalesPromotion'
                    cursor.execute(sql)
                    SalesPromotionid = cursor.fetchone()[0]
                    SalesPromotionid = str(int(SalesPromotionid)+1)

                    sql = 'INSERT INTO SalesPromotion(SalesPromotionID,SalesPromotionName,SellerID,startdate,enddate,discount) VALUES (%s,%s,%s,%s,%s,%s)'
                    cursor.execute(sql, [SalesPromotionid, SalesPromotionName, user.username, startdate, enddate, discount_scale])
                    conn.commit()
                    return JsonResponse({'code':0})

            elif modify_type == 1:
                PromotionId = data_json.get('PromotionId')
                PromotionName = data_json.get('PromotionName')
                startTime = data_json.get('startTime')
                endTime = data_json.get('endTime')
                discount = float(data_json.get('discount'))

                present_time =time.strptime(datetime.datetime.now().strftime('%Y-%m-%d'),'%Y-%m-%d')
                max_time = time.strptime('2099-12-31', '%Y-%m-%d')

                if discount < 0 or discount > 1:
                    return JsonResponse({'errmsg': '非法信息！折扣需在0-1之间','code':-1})
                elif endTime < startTime:
                    return JsonResponse({'errmsg': '非法信息！开始时间需在结束时间之后','code':-1})
                elif time.strptime(endTime, '%Y-%m-%d') > max_time:
                    return JsonResponse({'errmsg': '非法信息！结束时间需在2099-12-31以前','code':-1})

                else:
                    sql = 'UPDATE SalesPromotion SET  SalesPromotionName = %s, startdate = %s, enddate = %s, discount = %s WHERE SalesPromotionID = %s AND SellerID = %s'
                    cursor.execute(sql, [ PromotionName, startTime, endTime, discount, PromotionId, user.username])
                    conn.commit()
                    return JsonResponse({'code':0})


            elif modify_type == 2:
                PromotionId = data_json.get('PromotionId')

                # seller_delete_SalesPromotion(SalesPromotionid, cursor)
                sql = 'DELETE FROM SalesPromotion WHERE SalesPromotionID = %s'
                cursor.execute(sql, [PromotionId])
                conn.commit()
                return  JsonResponse({'code':0})

            else:
                return JsonResponse({'errmsg': '非法请求','code':-1})

        else:
            return JsonResponse({'errmsg': '非法定买家！请重新登录','code':-1})

