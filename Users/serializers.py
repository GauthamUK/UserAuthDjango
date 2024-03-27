from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password']

class UserVerificationSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    otp               = serializers.CharField()

class UserLoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    otp               = serializers.CharField()

class ForgotPasswordSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()

class ResetPasswordSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    otp               = serializers.CharField()
