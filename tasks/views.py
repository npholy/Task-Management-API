from rest_framework import generics
from .models import Task
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwner
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.filters import SearchFilter
from .pagination import TaskPagination

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
