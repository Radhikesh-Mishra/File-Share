# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser, UploadedFile
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from itsdangerous import URLSafeSerializer
from django.conf import settings
from rest_framework import status
import os

SECRET_KEY = "supersecret"  # use settings.SECRET_KEY in production

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            s = URLSafeSerializer(SECRET_KEY)
            encrypted_url = s.dumps(user.email)
            # Simulate email
            verification_url = f"http://localhost:8000/verify-email/{encrypted_url}"
            return Response({"verify_url": verification_url})
        return Response(serializer.errors, status=400)

class EmailVerifyView(APIView):
    def get(self, request, token):
        s = URLSafeSerializer(SECRET_KEY)
        try:
            email = s.loads(token)
            user = CustomUser.objects.get(email=email)
            user.email_verified = True
            user.save()
            return Response({"message": "Email verified"})
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class LoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=400)

class UploadFileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_ops:
            return Response({"error": "Only Ops User can upload"}, status=403)
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)

class ListFilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_client:
            return Response({"error": "Only Clients can view files"}, status=403)
        files = UploadedFile.objects.all()
        return Response([f.file.name for f in files])

class GenerateDownloadLinkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        if not request.user.is_client:
            return Response({"error": "Only Clients can download files"}, status=403)
        try:
            file = UploadedFile.objects.get(id=file_id)
            s = URLSafeSerializer(SECRET_KEY)
            token = s.dumps({"file_id": file_id, "user": request.user.id})
            return Response({"download-link": f"/download-file/{token}", "message": "success"})
        except UploadedFile.DoesNotExist:
            return Response({"error": "File not found"}, status=404)

class DownloadFileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token):
        s = URLSafeSerializer(SECRET_KEY)
        try:
            data = s.loads(token)
            if request.user.id != data['user']:
                return Response({"error": "Unauthorized"}, status=403)
            file = UploadedFile.objects.get(id=data['file_id'])
            with open(file.file.path, 'rb') as f:
                return Response(f.read(), content_type="application/octet-stream")
        except Exception as e:
            return Response({"error": str(e)}, status=400)
