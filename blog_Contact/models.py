from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import pytz




class BlogComment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        # managed = False
        db_table = 'blog_comment'

    def save(self, *args, **kwargs):
        georgia_timezone = pytz.timezone('Asia/Tbilisi')

        if not self.created_at:
            self.created_at = timezone.now().astimezone(georgia_timezone)

        super().save(*args, **kwargs)

class ContactMessage(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    content = models.CharField(max_length=500)

    class Meta:
        # managed = False
        db_table = 'contact_message'