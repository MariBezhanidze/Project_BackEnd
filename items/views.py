from rest_framework import generics, status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ItemList, Cart, Order
from .serializers import OrderSerializerTest, ItemSerializer, RegistrationSerializer, LoginSerializer, CartSerializer, OrderSerializer, UserSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User



# Create your views here.

class ItemListAPIView(generics.ListAPIView):
    queryset = ItemList.objects.all()
    serializer_class = ItemSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = ItemList.objects.all()
    serializer_class = ItemSerializer

    def get_object(self):
        try:
            return super().get_object()
        except ItemList.DoesNotExist:
            raise NotFound(detail="Product not found")


class ProductUpdate(generics.RetrieveUpdateAPIView):
    queryset = ItemList.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]


class CartItemDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()

    def get_object(self):
        user = self.request.user
        product_id = self.kwargs['cart_item_id']
        try:
            return self.get_queryset().get(product_id=product_id, customer_id=user)
        except Cart.DoesNotExist:
            raise NotFound("Cart item not found")



class ItemSearch(generics.ListAPIView):
    queryset = ItemList.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        category_query = self.request.query_params.getlist('category', [])
        min_price_query = self.request.query_params.get('min_price')
        max_price_query = self.request.query_params.get('max_price')
        material_query = self.request.query_params.getlist('material', [])
        min_size_query = self.request.query_params.get('min_size')
        max_size_query = self.request.query_params.get('max_size')

        filters = Q()

        if category_query:
            filters &= Q(category__in=category_query)

        if min_price_query:
            try:
                filters &= Q(price__gte=float(min_price_query))
            except ValueError:
                raise ParseError("Invalid 'min_price'. Must be a number.")
        if max_price_query:
            try:
                filters &= Q(price__lte=float(max_price_query))
            except ValueError:
                raise ParseError("Invalid 'max_price'. Must be a number.")

        if material_query:
            filters &= Q(material__in=material_query)

        if min_size_query:
            try:
                filters &= Q(size__gte=float(min_size_query))
            except ValueError:
                raise ParseError("Invalid 'min_size'. Must be a number.")
        if max_size_query:
            try:
                filters &= Q(size__lte=float(max_size_query))
            except ValueError:
                raise ParseError("Invalid 'max_size'. Must be a number.")

        queryset = queryset.filter(filters).order_by('price')
        return queryset



class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            cart = serializer.data.get("cart", [])

            for item in cart:
                cart_item, created = Cart.objects.get_or_create(
                    customer=user,
                    product_id=item["id"],
                    defaults={"product_amount": item["count"]}
                )

                if not created:
                    cart_item.product_amount += item["count"]
                    cart_item.save()

            refresh = RefreshToken.for_user(user)
            data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_id': user.id,
            }

            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')

            if not refresh_token:
                return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCartView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Cart.objects.filter(customer=user)


class UserCartUpdate(generics.UpdateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        product_id = self.kwargs.get("product_id")

        cart, created = Cart.objects.get_or_create(
            customer=user,
            product_id=product_id,
            defaults={"product_amount": 0}
        )
        return cart

    def update(self, request, *args, **kwargs):
        cart = self.get_object()
        product_amount = request.data.get("product_amount")

        if product_amount is not None:
            cart.product_amount += product_amount
            cart.save()

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

class UserCartUpdateBasket(generics.UpdateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        product_id = self.kwargs.get("product_id")

        cart, created = Cart.objects.get_or_create(
            customer=user,
            product_id=product_id,
            defaults={"product_amount": 0}
        )
        return cart

    def update(self, request, *args, **kwargs):
        cart = self.get_object()
        product_amount = request.data.get("product_amount")

        if product_amount is not None:
            cart.product_amount = product_amount
            cart.save()

        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class OrderCreate(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class UserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except user.DoesNotExist:
            raise NotFound(detail="User not found")

        serializer = UserSerializer(user)

        return Response(serializer.data)


class UserOrderView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializerTest

    def get_queryset(self):
        user = self.request.user
        if not user:
            raise NotFound(detail="User not found")

        return Order.objects.filter(customer=user)

