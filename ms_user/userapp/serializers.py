from rest_framework import serializers
from .models import User , Chat , Message

class UserSerializer(serializers.ModelSerializer):
    class Meta : 
        model = User
        fields = '__all__'
        
        
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"