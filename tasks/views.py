from rest_framework import generics
from .models import Task, Category
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwner
from .serializers import TaskSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.filters import SearchFilter
from .pagination import TaskPagination
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import AllowAny


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    pagination_class = TaskPagination

    # Only return tasks of the logged-in user
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    # Save the owner when creating a new task
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['completed']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']

class TaskRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]