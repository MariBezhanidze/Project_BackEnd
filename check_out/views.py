from rest_framework import generics
from rest_framework.exceptions import NotFound
from .models import OrderDetail
from .serializers import OrderDetailSerializer
from rest_framework.permissions import IsAuthenticated


class OrderDetailCreateApiView(generics.CreateAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]


class OrderDetailApiView(generics.ListAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = OrderDetail.objects.filter(user=user)

        if not queryset.exists():
            raise NotFound(detail="No order details found for this user.")

        return queryset

