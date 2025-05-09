# api/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_ops = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

class UploadedFile(models.Model):
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
