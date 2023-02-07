from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter

from utils.pagination import StandardResultsSetPagination
from .filters import IsOwnerFilterBackend
from .models import Task

from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all().order_by('id')
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [IsOwnerFilterBackend, SearchFilter]
    pagination_class = StandardResultsSetPagination
    search_fields = ['description']

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class TaskUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [IsOwnerFilterBackend]