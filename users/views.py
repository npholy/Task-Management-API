from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse

class UserCreateView(generics.CreateAPIView):
    """
    View for user registration.
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@ensure_csrf_cookie
def get_csrf_token(request):
    """
    Endpoint to set CSRF token cookie for the frontend.
    """
    return HttpResponse(status=200)