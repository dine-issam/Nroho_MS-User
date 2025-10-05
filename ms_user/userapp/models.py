from django.db import models

class User(models.Model):
    firebase_uid = models.CharField(max_length=128, unique=True, null=True, blank=True)
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    plan = models.CharField(max_length=50, default="FREE")

    def __str__(self):
        return self.email

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats")
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Message(models.Model):
    USER = "user"
    CHATBOT = "chatbot"
    FROM_CHOICES = [
        (USER, "User"),
        (CHATBOT, "Chatbot"),
    ]

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=FROM_CHOICES)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:30]}"
