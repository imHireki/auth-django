# Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from core.settings import SECRET_KEY

# App users
from .serializers import UserSerializer
from .models import User

# Packages for JWT
import jwt
from datetime import datetime, timedelta


class RegisterView(APIView):
    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, *args, **kwargs):
        email = self.request.data['email']
        password = self.request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow()
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        response = Response()

        response.set_cookie(
            key='jwt', value=token, httponly=True
        )

        response.data = {
            'jwt': token
        }
        return response
