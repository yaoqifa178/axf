from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'axf'
urlpatterns = [
    path('home/', views.home, name='home'),
    url(r'market/(\d+)/(\d+)/(\d+)/', views.market, name='market'),
    path('cart/', views.cart, name='cart'),
    path('mine/', views.mine, name='mine'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('checkuserid/', views.checkuserid, name='checkuserid'),
    path('quit/', views.quit, name='quit'),
    url(r'changecart/(\d+)/', views.changecart, name='changecart'),
    path('saveorder/', views.saveorder, name='saveorder'),
    path('oldorder/', views.oldorder, name='oldorder')
]
