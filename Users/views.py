from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *



class UserRegistrationView(APIView):
    def post(self,request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserVerificationView(APIView):
    def post(self, request):
        serializer = UserVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email_or_username = serializer.validated_data.get('email_or_username')
            otp = serializer.validated_data.get('otp')

            user = User.objects.filter(email=email_or_username).first() \
                   or User.objects.filter(username=email_or_username).first()

            if user and user.verify_otp(otp):
                user.is_verified = True
                user.save()
                return Response({'message': 'User verified successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email_or_username = serializer.validated_data.get('email_or_username')
            otp = serializer.validated_data.get('otp')

            user = User.objects.filter(email=email_or_username).first() \
                   or User.objects.filter(username=email_or_username).first()

            if user and user.verify_otp(otp):
                access_token = user.generate_access_token()
                refresh_token = user.generate_refresh_token()

                return Response({
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email_or_username = serializer.validated_data.get('email_or_username')

            user = User.objects.filter(email=email_or_username).first() \
                   or User.objects.filter(username=email_or_username).first()

            if user:
                otp = user.generate_otp()

                user.send_otp(otp)


                return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email_or_username = serializer.validated_data.get('email_or_username')
            otp = serializer.validated_data.get('otp')

            user = User.objects.filter(email=email_or_username).first() \
                   or User.objects.filter(username=email_or_username).first()

            if user and user.verify_otp(otp):
                new_password = serializer.validated_data.get('new_password')
                user.set_password(new_password)
                user.save()

                return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)