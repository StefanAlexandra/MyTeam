from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Q
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from task.filters import TaskFilters
from task.forms import TaskForm, TaskStatusUpdateForm
from task.models import Task
from userextend.decorators import manager_required

User = get_user_model()


@method_decorator([manager_required], name='dispatch')
class TaskCreateView(LoginRequiredMixin, CreateView):
    template_name = 'task/assign_task.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')


class TaskListView(LoginRequiredMixin, ListView):
    template_name = 'task/tasks.html'
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user

        if user.is_manager:
            return Task.objects.filter(
                Q(assigned_to=user) | Q(assigned_to__userprofile__superior=user)
            ).prefetch_related(Prefetch(
                'assigned_to', queryset=User.objects.select_related('userprofile')
            ))
        else:
            return Task.objects.filter(
                Q(assigned_to=user) | Q(assigned_to__isnull=True)
            ).prefetch_related(Prefetch(
                'assigned_to', queryset=User.objects.select_related('userprofile')
            ))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        tasks = self.get_queryset()
        task_filters = TaskFilters(self.request.GET, queryset=tasks)
        tasks = task_filters.qs
        data['tasks'] = tasks
        data['form_filters'] = task_filters.form

        return data


class TaskDetailView(LoginRequiredMixin, DetailView):
    template_name = 'task/task_details.html'
    model = Task


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'task/update_task.html'
    model = Task
    success_url = reverse_lazy('tasks')

    def get_form_class(self):
        user = self.request.user
        if user.is_manager:
            return TaskForm
        elif user.is_member:
            return TaskStatusUpdateForm


@method_decorator([manager_required], name='dispatch')
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'task/delete_task.html'
    model = Task
    success_url = reverse_lazy('tasks')
