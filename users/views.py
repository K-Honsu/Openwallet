from .serializer import UserSerializer, UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView
User = get_user_model()


class UserRegister(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = serializer.validated_data['password']
        user = serializer.save()
        user.set_password(password)
        user.save()
