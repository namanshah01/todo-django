from django.contrib import admin
from django.urls import path
from .views import listTask, updateTask, deleteTask, statusTask

urlpatterns = [
    path('', listTask, name='task-home'),
	path('update/<int:pk>/', updateTask, name='task-update'),
	path('delete/<int:pk>/', deleteTask, name='task-delete'),
	path('task/<int:pk>/', statusTask, name='task-status'),
]

