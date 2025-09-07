from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from tasks.views import CategoryViewSet, TaskViewSet, index, UserRegistrationView # We now import the 'index' view and 'UserRegistrationView'
from django.contrib.auth.views import LoginView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', index, name='index'), 
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/users/register/', UserRegistrationView.as_view(), name='register_user'), # New registration endpoint
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(template_name='index.html'), name='login'),
]
