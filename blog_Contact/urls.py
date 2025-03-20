from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import CommentCreateAPIView, CommentView, MessageCreateAPIView


urlpatterns = [
    path('comment_post/', CommentCreateAPIView.as_view()),
    path('comment_view/', CommentView.as_view()),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('post_message/', MessageCreateAPIView.as_view())
]
