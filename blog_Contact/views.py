from rest_framework import generics, status
from rest_framework.response import Response
from .models import BlogComment
from .serializer import CommentSerializer, CommentViewSerializer, ContactMessageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class CommentCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            blog_comment = serializer.save()
            return Response({
                'data': serializer.data,
                'status': status.HTTP_201_CREATED
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentView(generics.ListAPIView):
    queryset = BlogComment.objects.all()
    serializer_class = CommentViewSerializer


class MessageCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ContactMessageSerializer









