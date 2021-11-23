from django.urls import path

from . import views

#app_name = 'apps.shopping_platform'

urlpatterns = [
    path('', views.index, name='index'),
]