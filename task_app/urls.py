from django.urls import path

from .views import TaskListCreateView, TaskUpdateDestroyView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskUpdateDestroyView.as_view(), name='task-create'),
]