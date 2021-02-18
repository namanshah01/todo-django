from django.contrib import admin
from django.urls import path
from .views import statusTask, TaskCreateView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('', TaskCreateView.as_view(), name='task-home'),
	path('update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
	path('delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
	path('task/<int:pk>/', statusTask, name='task-status'),
]
