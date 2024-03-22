from rest_framework import serializers

from .models import NewUser, OnlineUser, ChatRoom, ChatMessage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ["id", "image", "username", "email"]
        extra_kwargs = {"id": {"read_only": True}}

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = NewUser
        fields = ["email", "username", "password", "password2", "image"]

    def create(self, validated_data):
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password")
        password2 = validated_data.get("password2")
        image = validated_data.get("image")

        if password == password2:
            user = NewUser(username=username, email=email, image=image)
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({"error": "Both password do not match"})

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = NewUser
        fields = ["email", "password"]

class ChatRoomSerializer(serializers.ModelSerializer):
    pass
