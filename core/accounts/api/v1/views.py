from django.core.mail import send_mail

from mail_templated import EmailMessage

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError


from django.shortcuts import get_object_or_404
from django.conf import settings

from accounts.models import User, Profile
from ..utils import EmailThread

from .serializers import (RegistrationSerializer, 
                          CustomAuthTokenSerializer,
                          CustomTokenObtainSerializer,
                          ChangePasswordSerializer,
                          ProfileSerializer,
                          ActivationResendSerializer)


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            data = {
                'email': email
            }
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            # MultiThreading Email sending Process.
            email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'mohsen@mohsen.com', to=[email])
            EmailThread(email_obj).start()

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
        })
    

class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer




class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # check old password:
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get:
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({'details': "password changed successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    # Get object without look_up_field (overwriting get_object)
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
    


class TestEmailSend(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        # Getting User's email for activation.
        self.email = "mohsentestuser@mohsen.com"
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_tokens_for_user(user_obj)

        # MultiThreading Email sending Process.
        email_obj = EmailMessage('email/hello.tpl', {'token': token}, 'mohsen@mohsen.com', to=[self.email])
        EmailThread(email_obj).start()
        return Response("email sent!")
    

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)




class ActivationAPIView(generics.GenericAPIView):
    def get(self, request, token, *args, **kwargs):
        # Token generated by simple-jwt-django-rest-framework or any
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response({"details": "token has been expired!"}, status=status.HTTP_400_BAD_REQUEST)
        except DecodeError:
            return Response({"details": "token has problem inside its self!"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_obj = User.objects.get(pk=user_id)
        user_obj.is_verified = True
        if user_obj.is_verified:
            return Response({"details": "your account has already been verified"})
        user_obj.save()
        return Response({"details": "your account has been verified and activated successfully."})
    

class ActivationResendAPIView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data['user']
        token = self.get_tokens_for_user(user_obj)

        # MultiThreading Email sending Process.
        email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'mohsen@mohsen.com', to=[user_obj.email])
        EmailThread(email_obj).start()
        return Response({"details": "user activation resend successfully!"}, status=status.HTTP_200_OK)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
