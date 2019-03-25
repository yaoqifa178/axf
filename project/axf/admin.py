from django.contrib import admin
from .models import Wheel, Nav, Mustbbuy, Shop, FoodType, Goods, User, Cart, Order

# Register your models here.


@admin.register(Wheel)
class AdminWhell(admin.ModelAdmin):
    list_display = ['img', 'name', 'trackid', 'isDelete']
    list_per_page = 5


@admin.register(Nav)
class AdminNav(admin.ModelAdmin):
    list_display = ['img', 'name', 'trackid', 'isDelete']
    list_per_page = 5


@admin.register(Mustbbuy)
class AdminMustbbuy(admin.ModelAdmin):
    list_display = ['img', 'name', 'trackid', 'isDelete']
    list_per_page = 5


@admin.register(Shop)
class AdminShop(admin.ModelAdmin):
    list_display = ['img', 'name', 'trackid', 'isDelete']
    list_per_page = 5


@admin.register(FoodType)
class AdminFoodType(admin.ModelAdmin):
    list_display = ['typeid', 'typename', 'typesort', 'childtypenames']
    list_per_page = 10


@admin.register(Goods)
class AdminGoods(admin.ModelAdmin):
    list_display = ['productid', 'productimg', 'productname', 'productlongname',
                    'isxf', 'pmdesc', 'specifics', 'price', 'marketprice', 'categoryid',
                    'childcid', 'childcidname', 'dealerid', 'storenums', 'productnum']
    list_per_page = 10


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['userAccount', 'userPassword', 'userName', 'userphone', 'userAddress',
                    'userImg', 'userRank', 'userToken']
    list_per_page = 5
    search_fields = ['userName']
    actions_on_top = False
    actions_on_bottom = True


@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ['userAccount', 'productid', 'productnum', 'productprice', 'isChose',
                    'productimg', 'productname', 'orderid', 'isDelete']
    list_per_page = 5


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['orderid', 'userid', 'progress']
    list_per_page = 10

