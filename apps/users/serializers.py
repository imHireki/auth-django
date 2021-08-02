"""
Serializer for users app

UserSerializer serializing User model
"""

# Django Rest Framework
from rest_framework import serializers

# Users app
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']

        # To not show the pass when create is called
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        """ Hash the password """
        password = validated_data.pop('password', None)
        # validated_data without pass
        instance = self.Meta.model(**self.validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance
