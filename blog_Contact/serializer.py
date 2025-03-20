import pytz
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import DateTimeField
from .models import BlogComment, ContactMessage


class CommentSerializer(serializers.ModelSerializer):
    created_at = DateTimeField(read_only=True)
    class Meta:
        model = BlogComment
        fields = ['content', 'created_at']

    def create(self, validated_data):
        user_instance = self.context['request'].user
        return BlogComment.objects.create(user=user_instance, content=validated_data['content'])

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        georgia_timezone = pytz.timezone('Asia/Tbilisi')

        created_at = instance.created_at.astimezone(georgia_timezone)
        formatted_created_at = created_at.strftime('%Y-%m-%dT%H:%M:%S')

        representation['created_at'] = formatted_created_at

        user = instance.user
        representation['user_name'] = f"{user.first_name} {user.last_name}"

        return representation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'id']


class CommentViewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = BlogComment
        fields = ['user', 'content', 'created_at']

    def get_created_at(self, obj):
        georgia_timezone = pytz.timezone('Asia/Tbilisi')

        created_at_in_georgia = obj.created_at.astimezone(georgia_timezone)

        return created_at_in_georgia.strftime('%Y-%m-%dT%H:%M:%S')


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"


