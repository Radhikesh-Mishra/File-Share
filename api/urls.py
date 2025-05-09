# api/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('verify-email/<str:token>/', EmailVerifyView.as_view()),
    path('login/', LoginView.as_view()),
    path('upload-file/', UploadFileView.as_view()),
    path('list-files/', ListFilesView.as_view()),
    path('generate-link/<int:file_id>/', GenerateDownloadLinkView.as_view()),
    path('download-file/<str:token>/', DownloadFileView.as_view()),
]
