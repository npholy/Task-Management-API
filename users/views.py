from rest_framework import generics
from .serializers import UserRegisterSerializer
from rest_framework.permissions import AllowAny

from .models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
