from django.urls import path
from . import views

urlpatterns = [
    # ---------------- USERS ----------------
    path("users/", views.getData, name="user-list"),
    path("users/create/", views.addUser, name="user-create"),
    path("users/<int:pk>/", views.getUser, name="user-detail"),
    path("users/update/<int:pk>/", views.updateUser, name="user-update"),
    path("users/delete/<int:pk>/", views.deleteUser, name="user-delete"),

    # ---------------- AUTH ----------------
    path("auth/signup/", views.signup, name="signup"),
    path("auth/signin/", views.signin, name="signin"),

    # ---------------- CHATS ----------------
    path("chats/", views.getChats, name="chat-list"),
    path("chats/create/", views.addChat, name="chat-create"),
    path("chats/<int:pk>/", views.getChat, name="chat-detail"),
    path("chats/update/<int:pk>/", views.updateChat, name="chat-update"),
    path("chats/delete/<int:pk>/", views.deleteChat, name="chat-delete"),

    # ---------------- MESSAGES ----------------
    path("messages/", views.getMessages, name="message-list"),
    path("messages/chat/<int:chat_id>/", views.getMessages, name="message-list-by-chat"),
    path("messages/create/", views.addMessage, name="message-create"),
    path("messages/<int:pk>/", views.getMessage, name="message-detail"),
    path("messages/update/<int:pk>/", views.updateMessage, name="message-update"),
    path("messages/delete/<int:pk>/", views.deleteMessage, name="message-delete"),
]
