# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import get_user_model
# import mysql.connector
# User = get_user_model()
#
#
# #%%
# @receiver(post_save, sender=User)
# def create_user(sender, instance=None, created=False, **kwargs):
#     if created:
#         password = instance.password
#         instance.set_password(password)
#         instance.save()
#
#         conn = mysql.connector.connect(host='localhost', user='root', password='root', database='onlineshoppingmall',auth_plugin = "mysql_native_password")
#         password = instance.password
#         username = instance.username
#         if instance.is_type == 0:
#             cursor = conn.cursor()
#             cursor.execute("INSERT INTO customer(CustomerId,CustomerPassword)"
#                                "values (%s,%s)", [username, password])
#             conn.commit()
#
#
#         if instance.is_type == 1:
#             cursor = conn.cursor()
#             cursor.execute("INSERT INTO seller (sellerid,sellerpassword)"
#                            "values (%s,%s)", [username, password])
#             conn.commit()




