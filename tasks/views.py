from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer, UserRegistrationSerializer
from .pagination import TaskPagination
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView

# This view is for serving the front-end HTML page.
def index(request):
    return render(request, 'index.html')

class UserRegistrationView(CreateAPIView):
    """
    A view for user registration.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

class TaskViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task instances.
    This viewset provides `list`, `create`, `retrieve`, `update`, `partial_update`, and `destroy` actions.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at']

    def get_queryset(self):
        """
        Return tasks for the authenticated user, filtered by query parameters.
        """
        user = self.request.user
        queryset = Task.objects.filter(owner=user).order_by('-created_at')
        
        # Apply filters from URL query parameters
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
            
        return queryset

    def perform_create(self, serializer):
        """
        Set the owner of the task to the current user.
        """
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['patch'])
    def toggle_status(self, request, pk=None):
        """
        Toggle the status of a specific task between 'todo' and 'done'.
        """
        task = self.get_object()
        if task.status == 'done':
            task.status = 'todo'
        else:
            task.status = 'done'
        task.save()
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return categories for the authenticated user, ordered by name.
        """
        return Category.objects.filter(owner=self.request.user).order_by('name')

    def perform_create(self, serializer):
        """
        Set the owner of the category to the current user.
        """
        serializer.save(owner=self.request.user)
