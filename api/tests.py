from django.test import TestCase

# Create your tests here.
# api/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import CustomUser, UploadedFile
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
from itsdangerous import URLSafeSerializer
from django.conf import settings

class FileSharingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.secret = settings.SECRET_KEY if hasattr(settings, "SECRET_KEY") else "testsecret"

        # Create Ops User
        self.ops_user = CustomUser.objects.create_user(
            username='opsuser',
            email='ops@example.com',
            password='ops123',
            is_ops=True,
            email_verified=True
        )
        self.ops_token = Token.objects.create(user=self.ops_user).key

        # Create Client User
        self.client_user = CustomUser.objects.create_user(
            username='clientuser',
            email='client@example.com',
            password='client123',
            is_client=True,
            email_verified=True
        )
        self.client_token = Token.objects.create(user=self.client_user).key

    def test_signup(self):
        response = self.client.post("/signup/", {
            "username": "newclient",
            "email": "newclient@example.com",
            "password": "clientpass"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("verify_url", response.data)

    def test_email_verification(self):
        s = URLSafeSerializer(self.secret)
        token = s.dumps("client@example.com")
        response = self.client.get(f"/verify-email/{token}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "Email verified")

    def test_login(self):
        response = self.client.post("/login/", {
            "username": "clientuser",
            "password": "client123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

    def test_file_upload_by_ops(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.ops_token)
        test_file = SimpleUploadedFile("test.docx", b"file_content", content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response = self.client.post("/upload-file/", {"file": test_file}, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("file" in response.data)

    def test_list_files_by_client(self):
        # Upload a file first
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.ops_token)
        test_file = SimpleUploadedFile("test.xlsx", b"file_content", content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.client.post("/upload-file/", {"file": test_file}, format='multipart')

        # List as client
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.client_token)
        response = self.client.get("/list-files/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.data, list))

    def test_generate_and_download_file(self):
        # Upload a file
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.ops_token)
        test_file = SimpleUploadedFile("test.pptx", b"slide_content", content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")
        upload_response = self.client.post("/upload-file/", {"file": test_file}, format='multipart')
        file_id = UploadedFile.objects.last().id

        # Generate download link
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.client_token)
        response = self.client.get(f"/generate-link/{file_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("download-link", response.data)

        # Use the download link
        token_link = response.data["download-link"].split("/")[-1]
        download_response = self.client.get(f"/download-file/{token_link}/")
        self.assertEqual(download_response.status_code, 200)
        self.assertEqual(download_response.content, b"slide_content")
