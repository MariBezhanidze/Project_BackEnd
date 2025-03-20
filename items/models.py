from rest_framework.pagination import PageNumberPagination
from django.db import models
from check_out.models import OrderDetail
from django.contrib.auth.models import User
# Create your models here.



class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100

class ItemList(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_title = models.TextField(max_length=20, blank=True, null=True)
    product_description = models.TextField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.CharField(max_length=1000, blank=True, null=True)
    img_alternative = models.CharField(max_length=1000, blank=True, null=True)
    material = models.CharField(max_length=20, blank=True, null=True)
    size = models.FloatField(max_length=5, blank=True, null=True)
    product_amount = models.IntegerField()
    category = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'item_list'
        managed = False

    def __str__(self):
        return self.product_title


class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(ItemList, on_delete=models.CASCADE)
    product_amount = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'cart'


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orders', null=True)
    products = models.ManyToManyField('ItemList', through='OrderProduct')
    total_price = models.IntegerField()
    address = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)

    class Meta:
        # managed = False
        db_table = 'orders'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name='order_products', null=True)
    product = models.ForeignKey(ItemList, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

    class Meta:
        # managed = False
        db_table = 'order_products'

