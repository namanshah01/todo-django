from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm

# Create your views here.

# @login_required
def listTask(request):
	tasks = Task.objects.all()
	form = TaskForm()
	if request.method == 'POST':
		form = TaskForm(request.POST)
		print('##### not validated #####')
		print(request.user)
		# print(form.instance.author)
		print(form.instance.title)
		print(form.instance.time)
		form.instance.author = request.user
		print(form.instance.author)
		if form.is_valid():
			form.save()
			print('##### validated #####')
			return redirect('/')
	context = {'tasks': tasks, 'form': form}
	return render(request, 'task/home.html', context)

class TaskCreateView(CreateView):
	model = Task
	fields = ['title']
	template_name = 'task/home.html'  # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	extra_context = {}

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	
	def get_success_url(self):
		return reverse('task-home')
	
	def get_context_data(self, *args, **kwargs):
		extra_context = super(TaskCreateView, self).get_context_data(*args, **kwargs)
		extra_context['tasks'] = Task.objects.all()
		return extra_context

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

