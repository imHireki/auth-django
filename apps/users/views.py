from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response


class RegisterView(APIView):
    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
