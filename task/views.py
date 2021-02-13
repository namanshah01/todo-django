from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

# Create your views here.

@login_required
def listTask(request):
	tasks = Task.objects.all()
	form = TaskForm()
	if request.method == 'POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'tasks': tasks, 'form': form}
	return render(request, 'task/home.html', context)

def updateTask(request, pk):
	task = Task.objects.get(id=pk)
	form = TaskForm(instance=task)

	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form': form}
	return render(request, 'task/update.html', context)

def deleteTask(request, pk):
	task = Task.objects.get(id=pk)
	if request.method == 'POST':
		task.delete()
		return redirect('/')
	context = {'task': task}
	return render(request, 'task/delete.html', context)

def statusTask(request, pk):
	task = Task.objects.get(id=pk)
	if task.complete == True:
		task.complete = False
	else:
		task.complete = True
	task.save()
	return redirect('/')

