📌 Django Realtime Chat App

A realtime chat application built with Django, Socket.IO, and Django REST Framework (DRF).
Supports group chat, text & image messages, and message history (pagination).

🚀 Features

🔐 Login + Room creation (username + room)

💬 Realtime group chat with Socket.IO

🖼️ Image sharing (upload + preview)

📜 Message history API with pagination

📂 Media file storage (/media/chat_images/)

📡 REST API for chat history (useful for infinite scroll or mobile apps)

🛠️ Tech Stack

Backend: Django, Django REST Framework, Socket.IO (ASGI)

Frontend: HTML, JS, Bootstrap (custom styles)

Database: SQLite (default) / PostgreSQL / MySQL

Realtime: Socket.IO

Optional Notifications: Firebase Cloud Messaging (FCM)

📂 Project Structure
realtime-chat/
│── chat/                  # Django app
│   ├── models.py          # Room, Message models
│   ├── views.py           # Login + Chat views
│   ├── urls.py            # App routes
│   ├── socketio_events.py # Socket.IO handlers
│   ├── templates/
│   │   ├── login.html
│   │   ├── chat.html
│   └── static/            # JS, CSS, images
│
│── config/              # Project settings
│   ├── settings.py
│   ├── urls.py
│
│── media/chat_images/     # Uploaded images
│── requirements.txt
│── README.md

⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/Toffan157/realtime-chat-django.git
cd chat-app

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate  # (Linux/macOS)
venv\Scripts\activate     # (Windows)

4️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Create Superuser (optional)
python manage.py createsuperuser

6️⃣ Run Development Server
python manage.py runserver


The app will be available at 👉 http://127.0.0.1:8000/

🔗 API Endpoints
Method	Endpoint	Description
GET	/chat/<room_name>/	Chat UI
GET	/chat/<room_name>/history/	Paginated message history
GET	/api/chat/<room_name>/messages/	REST API for messages
POST	/api/save-token/ (optional)	Save FCM token (notifications)
🖼️ Image Uploads

Images are stored in: media/chat_images/

Accessible via /media/chat_images/<filename>

Filenames use timestamp + random suffix → img_1735212345_ab12.png

📜 Example Message Object
{
  "id": 101,
  "username": "Alice",
  "content": "Hello World",
  "image": null,
  "content_type": "text",
  "timestamp": "2025-08-25T15:10:12.123Z"
}


For image messages:

{
  "id": 102,
  "username": "Bob",
  "content": null,
  "image": "/media/chat_images/img_1735212345_ab12.png",
  "content_type": "image",
  "timestamp": "2025-08-25T15:12:42.789Z"
}
