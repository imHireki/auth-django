from .models import User
from rest_framework import serializers


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
