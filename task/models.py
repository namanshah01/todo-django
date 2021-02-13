from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
	title = models.CharField(max_length=150)
	# detail = models.TextField(blank=True)
	complete = models.BooleanField(default=False)
	time = models.DateTimeField(auto_now_add=True)
	# time = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

