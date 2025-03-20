from django.db.models import Sum
from rest_framework import serializers
from check_out.models import OrderDetail
from check_out.serializers import OrderDetailSerializer
from .models import ItemList, Cart, Order, OrderProduct
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from collections import Counter
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemList
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    cart = serializers.ListField(child=serializers.IntegerField(), required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        cart_numbers = representation.get('cart', [])

        counter = Counter(cart_numbers)

        result = [{"id": num, "count": count} for num, count in counter.items()]

        representation['cart'] = result

        if 'password' in representation:
            del representation['password']

        return representation

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])

        if user is None:
            raise ValidationError("Invalid username or password.")

        if not user.is_active:
            raise ValidationError("This account is inactive.")

        data['user'] = user

        return data


class CartSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.product_title')
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    class Meta:
        model = Cart
        fields = ['customer', 'product', 'product_amount', 'product_title', 'product_price']


class UserSerializer(serializers.ModelSerializer):
    cart = CartSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['cart', 'first_name', 'last_name', 'id']


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'amount']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, source='order_products')
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    address = serializers.PrimaryKeyRelatedField(queryset=OrderDetail.objects.all())

    class Meta:
        model = Order
        fields = ['customer', 'address', 'total_price', 'products']

    def create(self, validated_data):
        products_data = validated_data.pop('order_products')
        order = Order.objects.create(**validated_data)
        for product_data in products_data:
            OrderProduct.objects.create(order=order, **product_data)
        return order


class OrderProductSerializerTest(serializers.ModelSerializer):
    product = ItemSerializer()
    class Meta:
        model = OrderProduct
        fields = ['product', 'amount']


class OrderSerializerTest(serializers.ModelSerializer):
    products = OrderProductSerializerTest(many=True, source='order_products')
    customer = UserSerializer()
    address = OrderDetailSerializer()
    class Meta:
        model = Order
        fields = ['id', 'customer', 'address', 'total_price', 'products']
