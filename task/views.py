from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
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

def check_user(user, task):
	print('## here ##')
	if task.author == request.user:
		return True
	return False

class TaskCreateView(LoginRequiredMixin, CreateView):
	model = Task
	fields = ['title']
	template_name = 'task/home.html'  # <app>/<model>_<viewtype>.html
	context_object_name = 'tasks'
	extra_context = {}

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	
	def get_success_url(self):
		return reverse('task-home')
	
	def get_context_data(self, *args, **kwargs):
		extra_context = super(TaskCreateView, self).get_context_data(*args, **kwargs)
		extra_context['tasks'] = Task.objects.filter(author=self.request.user)
		return extra_context

@user_passes_test(check_user, login_url='/login/')
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

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Task
	fields = ['title', 'complete']
	template_name = 'task/update.html'  # <app>/<model>_<viewtype>.html
	context_object_name = 'task'
	# success_url = reverse('task-home')

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	
	def get_success_url(self):
		return reverse('task-home')
	
	def test_func(self):
		task = self.get_object()
		if self.request.user == task.author:
			return True
		return False

def deleteTask(request, pk):
	task = Task.objects.get(id=pk)
	if request.method == 'POST':
		task.delete()
		return redirect('/')
	context = {'task': task}
	return render(request, 'task/delete.html', context)

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Task
	fields = ['title', 'complete']
	template_name = 'task/delete.html'  # <app>/<model>_<viewtype>.html
	context_object_name = 'task'
	# success_url = reverse('task-home')
	# extra_context = {'task': }
	
	def get_success_url(self):
		return reverse('task-home')
	
	def test_func(self):
		task = self.get_object()
		if self.request.user == task.author:
			return True
		return False

def statusTask(request, pk):
	task = Task.objects.get(id=pk)
	if task.complete == True:
		task.complete = False
	else:
		task.complete = True
	task.save()
	return redirect('/')

