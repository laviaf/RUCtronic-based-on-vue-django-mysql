# This is an auto-generated Django model module. You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(primary_key=True, max_length=50)
    USERNAME_FIELD = 'username'
    is_type = models.SmallIntegerField()


# class Chats(models.Model):
#     customerid = models.OneToOneField('Customer', models.DO_NOTHING, db_column='CustomerID', primary_key=True)  # Field name made lowercase.
#     sellerid = models.ForeignKey('Seller', models.DO_NOTHING, db_column='SellerID')  # Field name made lowercase.
#     texttime = models.DateTimeField(db_column='TextTime')  # Field name made lowercase.
#     content = models.CharField(db_column='Content', max_length=200, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'chats'
#         unique_together = (('customerid', 'sellerid', 'texttime'),)
#
#
# class Commodity(models.Model):
#     commodityid = models.CharField(db_column='CommodityID', primary_key=True, max_length=20)  # Field name made lowercase.
#     commodityname = models.CharField(db_column='CommodityName', unique=True, max_length=100, blank=True, null=True)  # Field name made lowercase.
#     commodityprofilephoto = models.CharField(db_column='CommodityProfilePhoto', max_length=100, blank=True, null=True)  # Field name made lowercase.
#     sellerid = models.ForeignKey('Seller', models.DO_NOTHING, db_column='SellerID', blank=True, null=True)  # Field name made lowercase.
#     salespromotionid = models.ForeignKey('Salespromotion', models.DO_NOTHING, db_column='SalesPromotionID', blank=True, null=True)  # Field name made lowercase.
#     commodity_description = models.CharField(db_column='Commodity_description', max_length=200, blank=True, null=True)  # Field name made lowercase.
#     commodityinventory = models.IntegerField(db_column='CommodityInventory', blank=True, null=True)  # Field name made lowercase.
#     commodityoriginalprice = models.IntegerField(db_column='CommodityOriginalPrice', blank=True, null=True)  # Field name made lowercase.
#     commodityprice = models.IntegerField(db_column='CommodityPrice', blank=True, null=True)  # Field name made lowercase.
#     commoditysalesvolume = models.IntegerField(db_column='CommoditySalesVolume', blank=True, null=True)  # Field name made lowercase.
#     commoditytype = models.CharField(db_column='CommodityType', max_length=20, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'commodity'
#
#
# class Customer(models.Model):
#     customerid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='CustomerId', primary_key=True, max_length=20)
#     # customerid = models.CharField(db_column='CustomerId', primary_key=True, max_length=20)
#     customername = models.CharField(db_column='CustomerName', max_length=100, blank=True, null=True)
#     customerprofilephoto = models.CharField(db_column='CustomerProfilePhoto', max_length=100, blank=True, null=True)  # Field name made lowercase.
#     customerlv = models.CharField(db_column='CustomerLV', max_length=10, blank=True, null=True)  # Field name made lowercase.
#     customeraddress = models.CharField(db_column='CustomerAddress', max_length=100, blank=True, null=True)  # Field name made lowercase.
#     customerbalance = models.IntegerField(db_column='CustomerBalance', blank=True, null=True)  # Field name made lowercase.
#     customertele = models.CharField(db_column='CustomerTELE', max_length=100, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'customer'
#
#
# class Favorites(models.Model):
#     customerid = models.OneToOneField(Customer, models.DO_NOTHING, db_column='CustomerID', primary_key=True)  # Field name made lowercase.
#     commodityid = models.ForeignKey(Commodity, models.DO_NOTHING, db_column='CommodityID')  # Field name made lowercase.
#     favoritesdate = models.DateField(db_column='FavoritesDate', blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'favorites'
#         unique_together = (('customerid', 'commodityid'),)
#
#
# class Orderform(models.Model):
#     orderid = models.CharField(db_column='OrderID', primary_key=True, max_length=20)  # Field name made lowercase.
#     sellerid = models.ForeignKey('Seller', models.DO_NOTHING, db_column='SellerID', blank=True, null=True)  # Field name made lowercase.
#     commodityid = models.ForeignKey(Commodity, models.DO_NOTHING, db_column='CommodityID', blank=True, null=True)  # Field name made lowercase.
#     customerid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CustomerID', blank=True, null=True)  # Field name made lowercase.
#     quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
#     unitprice = models.FloatField(db_column='UnitPrice', blank=True, null=True)  # Field name made lowercase.
#     orderdate = models.DateField(db_column='OrderDate', blank=True, null=True)  # Field name made lowercase.
#     orderexpressno = models.CharField(db_column='OrderExpressNO', max_length=20, blank=True, null=True)  # Field name made lowercase.
#     orderstate = models.CharField(db_column='OrderState', max_length=20, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'orderform'
#
#
# class Purchased(models.Model):
#     orderid = models.OneToOneField(Orderform, models.DO_NOTHING, db_column='OrderID', primary_key=True)  # Field name made lowercase.
#     comment = models.CharField(db_column='Comment', max_length=200, blank=True, null=True)  # Field name made lowercase.
#     rating = models.CharField(db_column='Rating', max_length=10, blank=True, null=True)  # Field name made lowercase.
#     purchasedstate = models.CharField(db_column='PurchasedState', max_length=10, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'purchased'
#
#
# class Salespromotion(models.Model):
#     salespromotionid = models.CharField(db_column='SalesPromotionID', primary_key=True, max_length=20)  # Field name made lowercase.
#     salespromotionname = models.CharField(db_column='SalesPromotionName', unique=True, max_length=100, blank=True, null=True)  # Field name made lowercase.
#     sellerid = models.ForeignKey('Seller', models.DO_NOTHING, db_column='SellerID', blank=True, null=True)  # Field name made lowercase.
#     startdate = models.DateField(blank=True, null=True)
#     enddate = models.DateField(blank=True, null=True)
#     salespromotion_description = models.CharField(db_column='SalesPromotion_description', max_length=200, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'salespromotion'
#
#
# class Seller(models.Model):
#     sellerid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='SellerID', primary_key=True, max_length=20)
#     # seuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_User', db_column='seuser_id')
#     # sellerid = models.CharField(db_column='SellerID', primary_key=True, max_length=20)  # Field name made lowercase.
#     sellername = models.CharField(db_column='SellerName', unique=True, max_length=100, blank=True, null=True)  # Field name made lowercase.
#     sellerlv = models.CharField(db_column='SellerLV', max_length=10, blank=True, null=True)  # Field name made lowercase.
#     selleraddress = models.CharField(db_column='SellerAddress', max_length=100, blank=True, null=True)  # Field name made lowercase.
#     sellertele = models.CharField(db_column='SellerTELE', max_length=100, blank=True, null=True)  # Field name made lowercase.
#     sellerpassword = models.CharField(db_column='SellerPassword', max_length=100, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'seller'
#
#
# class Shoppingcart(models.Model):
#     customerid = models.OneToOneField(Customer, models.DO_NOTHING, db_column='CustomerID', primary_key=True)  # Field name made lowercase.
#     commodityid = models.ForeignKey(Commodity, models.DO_NOTHING, db_column='CommodityID')  # Field name made lowercase.
#     commodityquantity = models.IntegerField(db_column='CommodityQuantity', blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'shoppingcart'
#         unique_together = (('customerid', 'commodityid'),)
#
#
# class Visitor(models.Model):
#     visitorid = models.CharField(db_column='VisitorID', primary_key=True, max_length=20)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'visitor'
