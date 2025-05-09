# api/serializers.py
from rest_framework import serializers
from .models import CustomUser, UploadedFile
from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.is_client = True
        user.save()
        return user

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['file']

    def validate_file(self, file):
        if not file.name.endswith(('.docx', '.pptx', '.xlsx')):
            raise serializers.ValidationError("Invalid file type")
        return file
