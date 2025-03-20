from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class OrderDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    card = models.IntegerField()

    class Meta:
        db_table = 'order_detail'
        # managed = False