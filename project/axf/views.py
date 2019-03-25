import os
import re

from django.contrib.auth import logout
from django.shortcuts import render, redirect

from axf.forms.login import LoginForm
from .models import Wheel, Nav, Mustbbuy, Shop, FoodType, Goods, User, Cart, Order
from django.http import JsonResponse
import time
import random
from django.conf import settings

# Create your views here.


def home(request):
    wheelsList = Wheel.objects.all()
    navList = Nav.objects.all()
    mustbuyList = Mustbbuy.objects.all()
    shopList = Shop.objects.all()
    shop1 = shopList[0]
    shop2 = shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:9]
    shop5 = shopList[9:11]

    return render(request, 'axf/home.html', {"title": "主页", 'wheelsList': wheelsList,
                                             'navList': navList, 'mustbuyList': mustbuyList,
                                             'shop1': shop1, 'shop2': shop2, 'shop3': shop3,
                                             'shop4': shop4, 'shop5': shop5})


def market(request, categoryid, cid, sortid):
    leftSlide = FoodType.objects.all()
    if cid == '0':
        productList = Goods.objects.filter(categoryid=categoryid)
    else:
        productList = Goods.objects.filter(categoryid=categoryid, childcid=cid)

    # 排序
    if sortid == '1':
        productList = productList.order_by('-productnum')
    elif sortid == '2':
        productList = productList.order_by("price")
    elif sortid == '3':
        productList = productList.order_by('-price')

    group = leftSlide.get(typeid=categoryid)
    childList = []
    childnames = group.childtypenames
    arr1 = childnames.split("#")
    for str in arr1:
        arr2 = str.split(":")
        obj = {"childName": arr2[0], "childId": arr2[1]}
        childList.append(obj)

    cartlist = []
    token = request.session.get('token')
    if token:
        user = User.objects.get(userToken=token)
        cartlist = Cart.objects.filter(userAccount=user.userAccount)
    for p in productList:
        for c in cartlist:
            if c.productid == p.productid:
                p.num = c.productnum
                continue

    return render(request, 'axf/market.html', {"title": "闪送超市", "leftSlide": leftSlide,
                                               "productList": productList, "childList": childList,
                                               'categoryid': categoryid, 'cid': cid})


def cart(request):
    token = request.session.get('token')
    cartlist = []
    user = []
    money = 0
    if token is not None:
        user = User.objects.get(userToken=token)
        cartlist = Cart.objects.filter(userAccount=user.userAccount)
        carts = cartlist.filter(isChose=True)
        for item in carts:
            money += item.productprice
        money = '%.2f' % money
    return render(request, 'axf/cart.html', {"title": "购物车", 'cartlist': cartlist,
                                             'user': user, 'money': money})


def mine(request):
    username = request.session.get('username', '点击登录')
    usertoken = request.session.get('token', '0')
    if (username == '点击登录')and(usertoken == '0'):
        userrank = 0
        userimg = '0'
    else:
        user = User.objects.get(userName=username, userToken=usertoken)
        userrank = user.userRank
        userimg = user.userImg
    return render(request, 'axf/mine.html', {"title": "我的", 'username': username,
                                             'userrank': userrank, 'userimg': userimg})


def login(request):  # 登录
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():
            # 信息格式没多大问题，验证账号和密码的正确性
            name = f.cleaned_data['username']
            pwd = f.cleaned_data['password']
            try:
                user = User.objects.get(userAccount=name)
                if user.userPassword != pwd:
                    return redirect('/login/')
            except User.DoesNotExist as e:
                return redirect('/login/')

            token = time.time() + random.randrange(1, 100000)
            user.userToken = str(token)
            user.save()
            request.session['username'] = user.userName
            request.session['token'] = user.userToken
            return redirect('/mine/')
        else:
            return render(request, 'axf/login.html', {'title': '登录', 'form': f, 'error': f.errors})
    else:
        f = LoginForm()
    return render(request, 'axf/login.html', {'title': '登录', 'form': f})


def register(request):
    if request.method == 'POST':
        userAccount = request.POST.get('userAccount')
        userPassword = request.POST.get('userPass')
        userName = request.POST.get('userName')
        userPass = request.POST.get('userPasswd')
        userphone = request.POST.get('userPhone')
        userAddress = request.POST.get('userAddress')
        userRank = 1
        token = time.time() + random.randrange(1, 100000)
        userToken = str(token)
        try:
            u = User.objects.get(userAccount=userAccount)
            return redirect('/register/')
        except User.DoesNotExist as e:
            if (userPass == userPassword)and(len(userPass) >= 6)and(len(userPass) <= 16) \
                    and (len(userAccount) >= 6)and(len(userAccount) <= 12):
                f = request.FILES['userImg']
                userImg = os.path.join(settings.MEDIA_ROOT, userAccount + f.name)
                with open(userImg, 'wb') as fp:
                    for data in f.chunks():
                        fp.write(data)
                print(userImg)
                userImg = re.search(r'\\static\\media\\(.*)', userImg, re.M | re.I)
                userImg = userImg.group(0)
                user = User.createuser(userAccount, userPassword, userName, userphone, userAddress,
                                       userImg, userRank, userToken)
                user.save()

                request.session['username'] = userName
                request.session['token'] = userToken

                return redirect('/mine/')
            else:
                return redirect('/register/')
    else:
        return render(request, 'axf/register.html', {'title': '注册'})


def checkuserid(request):
    userid = request.POST.get("userid")
    try:
        user = User.objects.get(userAccount=userid)
        return JsonResponse({'data': "该用户已经被注册", 'status': 'error'})
    except User.DoesNotExist as e:
        return JsonResponse({'data': 'ok', 'status': 'success'})


def quit(request):
    logout(request)
    return redirect('/mine/')


def changecart(request, flag):
    # 判断用户是否登录
    token = request.session.get('token', '0')
    if token == '0':
        return JsonResponse({'data': -1, 'status': 'error'})
    productid = request.POST.get('productid')
    user = User.objects.get(userToken=token)
    product = Goods.objects.get(productid=productid)
    orderid = '0'
    c = None
    if flag == '0':
        if product.storenums == 0:
            return JsonResponse({'data': -2, 'status': 'error'})
        carts = Cart.objects.filter(userAccount=user.userAccount)
        if carts.count() == 0:
            # 直接增加一条订单
            c = Cart.createcart(user.userAccount, productid, 1, product.price, False, product.productimg,
                                product.productlongname, orderid, False)
            c.save()
        else:
            try:
                c = carts.get(productid=productid)
                # 修改数量和价格
                c.productnum += 1
                c.productprice = c.productnum * product.price
                c.save()
            except Cart.DoesNotExist as e:
                # 直接增加一条订单
                c = Cart.createcart(user.userAccount, productid, 1, product.price, False, product.productimg,
                                    product.productlongname, orderid, False)
                c.save()
        product.storenums -= 1
        product.save()
        c.productprice = '%.2f' % c.productprice
        money = 0
        carts = carts.filter(isChose=True)
        for item in carts:
            money += item.productprice
        money = '%.2f' % money
        return JsonResponse({'data': c.productnum, 'price': c.productprice, 'price1': money, 'status': 'success'})

    elif flag == '1':
        carts = Cart.objects.filter(userAccount=user.userAccount)
        if carts.count() == 0:
            return JsonResponse({'data': -2, 'status': 'error'})
        else:
            try:
                c = carts.get(productid=productid)
                # 修改数量和价格
                c.productnum -= 1
                c.productprice = c.productnum * product.price
                if c.productnum == 0:
                    c.delete()
                else:
                    c.save()
            except Cart.DoesNotExist as e:
                return JsonResponse({'data': -2, 'status': 'error'})
        product.storenums += 1
        product.save()
        c.productprice = '%.2f' % c.productprice
        money = 0
        carts = carts.filter(isChose=True)
        for item in carts:
            money += item.productprice
        money = '%.2f' % money
        return JsonResponse({'data': c.productnum, 'price': c.productprice, 'price1': money, 'status': 'success'})
    elif flag == '2':
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = carts.get(productid=productid)
        c.isChose = not c.isChose
        c.save()
        str = ''
        if c.isChose:
            str = '√'
        money = 0
        carts = carts.filter(isChose=True)
        for item in carts:
            money += item.productprice
        money = '%.2f' % money
        return JsonResponse({'data': str, 'price1': money, 'status': 'success'})
    elif flag == '3':
        pass


def saveorder(request):
    token = request.session.get('token')
    if token is None:
        return JsonResponse({'data': -1, 'status': 'error'})
    user = User.objects.get(userToken=token)
    carts = Cart.objects.filter(isChose=True)
    if carts.count() == 0:
        return JsonResponse({'data': -1, 'status': 'error'})
    oid = time.time() + random.randrange(1, 10000)
    oid = '%d' % oid
    money = 0
    carts = carts.filter(isChose=True)
    for item in carts:
        money += item.productprice
    money = '%.2f' % money
    o = Order.createorder(oid, user.userAccount, money)
    o.save()
    for item in carts:
        item.isDelete = True
        item.orderid = oid
        item.save()
    return JsonResponse({'data': -1, 'status': 'success'})


def oldorder(requset):
    token = requset.session.get('token')
    orderlist = []
    orders = []
    if token is not None:
        user = User.objects.get(userToken=token)
        orders = Order.objects.filter(userid=user.userAccount)
        for item1 in orders:
            orderlists = Cart.obj.filter(orderid=item1.orderid)
            orderlist.extend(orderlists)
    return render(requset, 'axf/order.html', {'orderlist': orderlist, 'orders': orders})
