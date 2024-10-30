from rest_framework import serializers

from .models import Chat, User
from .utilities import chat_response


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'tokens'
        ]
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
            )
        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['user',
                  'message',
                  'response',
                  'timestamp'
                  ]
        readonly = [
                    'response',
                    'timestamp',
                    ]
        extra_kwargs = {'user' : {'write_only': True}}
        
    def create(self, validated_data):
        validated_data['response'] = chat_response(validated_data['message'])
        print('Creating chat!!!!')
        print(validated_data)
        return super().create(validated_data)
    
    # def create(self, validated_data):
    #     return super().create(validated_data)
    