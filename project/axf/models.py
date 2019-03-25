from django.db import models

# Create your models here.


class Wheel(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'wheel'


class Nav(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'nav'


class Mustbbuy(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'mustbuy'


class Shop(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'shop'


class FoodType(models.Model):
    typeid = models.CharField(max_length=10)
    typename = models.CharField(max_length=20)
    typesort = models.IntegerField()
    childtypenames = models.CharField(max_length=150)

    class Meta:
        db_table = 'foodtype'


class Goods(models.Model):
    # 商品id
    productid = models.CharField(max_length=10)
    # 图片
    productimg = models.CharField(max_length=150)
    # 名字
    productname = models.CharField(max_length=50)
    # 长名字
    productlongname = models.CharField(max_length=100)
    # 是否精选
    isxf = models.NullBooleanField(default=False)
    # 是否买一赠一
    pmdesc = models.CharField(max_length=10)
    # 规格
    specifics = models.CharField(max_length=20)
    # 价格
    price = models.FloatField()
    # 原价
    marketprice = models.FloatField()
    # 商品组id
    categoryid = models.CharField(max_length=10)
    # 商品子组id
    childcid = models.CharField(max_length=10)
    # 商品子组名名称
    childcidname = models.CharField(max_length=10)
    # 详情页id
    dealerid = models.CharField(max_length=10)
    # 库存
    storenums = models.IntegerField()
    # 销量
    productnum = models.IntegerField()

    class Meta:
        db_table = 'goods'


class User(models.Model):
    # 用户账号
    userAccount = models.CharField(max_length=20, unique=True)
    # 密码
    userPassword = models.CharField(max_length=20)
    # 昵称
    userName = models.CharField(max_length=20)
    # 手机号
    userphone = models.CharField(max_length=20)
    # 地址
    userAddress = models.CharField(max_length=100)
    # 头像路径
    userImg = models.CharField(max_length=150)
    # 等级
    userRank = models.IntegerField()
    # touken验证值，每次登录之后都会更新
    userToken = models.CharField(max_length=50)

    @classmethod
    def createuser(cls, account, password, name, phone, address, img, rank, token):
        u = cls(userAccount=account, userPassword=password, userName=name, userphone=phone,
                userAddress=address, userImg=img, userRank=rank, userToken=token)
        return u


class CartManage(models.Manager):
    def get_queryset(self):
        return super(CartManage, self).get_queryset().filter(isDelete=False)


class CartManage2(models.Manager):
    def get_queryset(self):
        return super(CartManage2, self).get_queryset().filter(isDelete=True)


class Cart(models.Model):
    userAccount = models.CharField(max_length=20)
    productid = models.CharField(max_length=10)
    productnum = models.IntegerField()
    productprice = models.FloatField()
    isChose = models.BooleanField(default=True)
    productimg = models.CharField(max_length=150)
    productname = models.CharField(max_length=100)
    orderid = models.CharField(max_length=20, default='0')
    isDelete = models.BooleanField(default=False)
    objects = CartManage()
    obj = CartManage2()

    @classmethod
    def createcart(cls, userAccount, productid, productnum, productprice, isChose,
                   productimg, productname, orderid, isDelete):
        c = cls(userAccount=userAccount, productid=productid, productnum=productnum,
                productprice=productprice, isChose=isChose,productimg=productimg,
                productname=productname, orderid=orderid, isDelete=isDelete)
        return c


class Order(models.Model):
    orderid = models.CharField(max_length=20)
    userid = models.CharField(max_length=20)
    progress = models.FloatField()

    @classmethod
    def createorder(cls, orderid, userid, progress):
        o = cls(orderid=orderid, userid=userid, progress=progress)
        return o

    class Meta:
        db_table = 'order'
