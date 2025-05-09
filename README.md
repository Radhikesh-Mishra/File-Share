# 📁 Django File Sharing App

This is a secure and minimal file-sharing application built using Django. It allows users to create accounts, upload files, generate secure download links, and manage their uploaded content with ease.

---

## 🚀 Features

- User registration with email verification
- Secure login system with token-based authentication
- File upload and listing per user
- Generation of secure download links for individual files
- Download functionality via tokenized URLs

---

## 📌 API Endpoints (urlpatterns)

Here are the available API routes and what each of them does:

### 🔐 User Authentication

- **`POST /signup/`**  
  Registers a new user account. Requires basic user details such as email, password, etc.  
  Triggers a verification email with a unique token.

- **`GET /verify-email/<str:token>/`**  
  Verifies the user's email using the token sent to their email address.  
  Example: `/verify-email/abc123token/`

- **`POST /login/`**  
  Authenticates a user and returns a token for further requests.  
  Requires email and password.

---

### 📤 File Operations

- **`POST /upload-file/`**  
  Allows an authenticated user to upload a file.  
  The file is stored on the server and associated with the user's account.

- **`GET /list-files/`**  
  Returns a list of all files uploaded by the currently logged-in user.  
  Includes file metadata such as name, size, upload date, and ID.

- **`GET /generate-link/<int:file_id>/`**  
  Generates a secure, temporary tokenized link to download a specific file.  
  Example: `/generate-link/12/` will return a download URL with a token.

- **`GET /download-file/<str:token>/`**  
  Enables the user to download a file using a valid token.  
  This route is token-protected and does not expose the original file path.  
  Example: `/download-file/token123xyz/`

---

### Some postman images
  ![WhatsApp Image 2025-05-09 at 8 38 13 PM](https://github.com/user-attachments/assets/e633ba8f-8148-4746-80ca-db1898a0aa65)
  ![WhatsApp Image 2025-05-09 at 8 39 04 PM](https://github.com/user-attachments/assets/aace0675-028b-4125-9bdb-1678012daba2)
  ![WhatsApp Image 2025-05-09 at 8 47 33 PM](https://github.com/user-attachments/assets/a4c28507-65b7-4c86-83d2-8262394b5af2)
