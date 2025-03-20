from django.urls import path
from .views import UserView, UserOrderView, ItemListAPIView, ItemSearch, RegisterAPIView, LoginAPIView, LogoutView, UserCartView, ProductDetailView, ProductUpdate, CartItemDeleteView, UserCartUpdate, UserCartUpdateBasket, OrderCreate


urlpatterns = [
    path('user/<int:pk>/', UserView.as_view()),
    path('all_items/', ItemListAPIView.as_view()),
    path('all_items/<int:pk>/', ProductDetailView.as_view()),
    path('all_items/<int:pk>/update/', ProductUpdate.as_view()),
    path('cart/item/<int:cart_item_id>/delete/', CartItemDeleteView.as_view()),
    path('cart/<int:product_id>/update/', UserCartUpdate.as_view()),
    path('cart/<int:product_id>/basket_update/', UserCartUpdateBasket.as_view()),
    path('order_create/', OrderCreate.as_view()),
    path('item_search/', ItemSearch.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('cart_view/', UserCartView.as_view()),
    path('order_view/<int:pk>/', UserOrderView.as_view()),
    path('logout/', LogoutView.as_view())
]
