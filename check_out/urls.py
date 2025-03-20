from django.urls import path
from .views import OrderDetailCreateApiView, OrderDetailApiView, OrderDetailUpdateApiView

urlpatterns = [
    path('address_create/', OrderDetailCreateApiView.as_view()),
    path('address/<int:pk>/', OrderDetailUpdateApiView.as_view()),
    path('address_view/', OrderDetailApiView.as_view()),
]