from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    TEXT = "text"
    IMAGE = "image"

    CONTENT_TYPES = [
        (TEXT, "Text"),
        (IMAGE, "Image"),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    username = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="chat_images/", blank=True, null=True)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default=TEXT)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.username} in {self.room.name}: {self.content[:20]}"
