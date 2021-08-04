"""
Views for users app
"""

# Django Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions

# Apps
from .serializers import UserSerializer
from .models import User
from core.settings import SECRET_KEY

# Packages for JWT
import jwt
from datetime import datetime, timedelta


class RegisterView(APIView):
    """
    Gets a POST request with the `user's registering data`.

    Returns the `user serialized`.
    """
    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    """
    Gets a POST request with the `user's login data`.

    Returns the `user's jwt token`
    """
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


class UserView(APIView):
    """
    Gets a GET request with the `user's jwt token`.

    Returns the `user's serialized and decoded jwt token`
    """
    def get(self, *args, **kwargs):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise exceptions.NotAuthenticated('Unauthenticated!')

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.NotAuthenticated('Unauthenticated!')
        
        user = User.objects.get(id=(payload['id']))
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    """
    Gets a POST request withe the `user's jwt token`
    
    Returns a `response` with a success message
    """
    def post(self, *args, **kwargs):
        token = self.request.COOKIES.get('jwt')
        if not token: raise exceptions.NotAcceptable

        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
        