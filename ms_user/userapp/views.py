import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from firebase_admin import auth
from .models import User , Chat , Message
from .serializers import UserSerializer , ChatSerializer , MessageSerializer


# ------------------- CRUD -------------------

@api_view(['GET'])
def getData(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUser(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
def addUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateUser(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteUser(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response({"message": "User successfully deleted!"}, status=status.HTTP_200_OK)


# ------------------- AUTH -------------------

@api_view(['POST'])
def signup(request):
    """ Create user in Firebase + save in Postgres """
    email = request.data.get("email")
    password = request.data.get("password")
    name = request.data.get("name")
    plan = request.data.get("plan", "FREE")

    if not email or not password:
        return Response({"error": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 1. Create user in Firebase
        fb_user = auth.create_user(email=email, password=password)

        # 2. Save in Postgres
        user = User.objects.create(
            firebase_uid=fb_user.uid,
            email=email,
            name=name,
            plan=plan
        )

        return Response({
            "id": user.id,   # use Django default pk
            "firebase_uid": user.firebase_uid,
            "email": user.email,
            "name": user.name,
            "plan": user.plan
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signin(request):
    """ Login user using Firebase REST API + return local user """
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 1. Call Firebase REST API
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={settings.FIREBASE_API_KEY}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        r = requests.post(url, json=payload)

        if r.status_code != 200:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        data = r.json()
        id_token = data["idToken"]
        refresh_token = data["refreshToken"]
        firebase_uid = data["localId"]

        # 2. Verify token with Firebase Admin
        auth.verify_id_token(id_token)

        # 3. Get user from Postgres
        try:
            user = User.objects.get(firebase_uid=firebase_uid)
        except User.DoesNotExist:
            return Response({"error": "User exists in Firebase but not in DB"}, status=status.HTTP_404_NOT_FOUND)

        # 4. Serialize and return response
        serializer = UserSerializer(user)
        return Response({
            "user": serializer.data,
            "idToken": id_token,
            "refreshToken": refresh_token
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from .models import User, Chat, Message
from .serializers import UserSerializer, ChatSerializer, MessageSerializer

# ------------------- CHAT CRUD -------------------

@api_view(['GET'])
def getChats(request):
    chats = Chat.objects.all()
    serializer = ChatSerializer(chats, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getChat(request, pk):
    try:
        chat = Chat.objects.get(id=pk)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ChatSerializer(chat)
    return Response(serializer.data)


@api_view(['POST'])
def addChat(request):
    serializer = ChatSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateChat(request, pk):
    try:
        chat = Chat.objects.get(id=pk)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ChatSerializer(instance=chat, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteChat(request, pk):
    try:
        chat = Chat.objects.get(id=pk)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)

    chat.delete()
    return Response({"message": "Chat successfully deleted!"}, status=status.HTTP_200_OK)


# ------------------- MESSAGE CRUD -------------------

@api_view(['GET'])
def getMessages(request, chat_id=None):
    """ If chat_id is provided, get only messages from that chat """
    if chat_id:
        messages = Message.objects.filter(chat_id=chat_id)
    else:
        messages = Message.objects.all()

    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getMessage(request, pk):
    try:
        message = Message.objects.get(id=pk)
    except Message.DoesNotExist:
        return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = MessageSerializer(message)
    return Response(serializer.data)


@api_view(['POST'])
def addMessage(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateMessage(request, pk):
    try:
        message = Message.objects.get(id=pk)
    except Message.DoesNotExist:
        return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = MessageSerializer(instance=message, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteMessage(request, pk):
    try:
        message = Message.objects.get(id=pk)
    except Message.DoesNotExist:
        return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)

    message.delete()
    return Response({"message": "Message successfully deleted!"}, status=status.HTTP_200_OK)
