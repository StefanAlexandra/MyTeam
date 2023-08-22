from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from project.filters import ProjectFilters
from project.forms import ProjectForm
from project.models import Project
from userextend.decorators import manager_required

User = get_user_model()


@method_decorator([manager_required], name='dispatch')
class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'project/add_project.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('projects')


class ProjectListView(LoginRequiredMixin, ListView):
    template_name = 'project/projects.html'
    model = Project
    context_object_name = 'projects'

    def get_queryset(self):
        user = self.request.user

        if user.is_manager:
            return Project.objects.filter(
                Q(members=user) | Q(members__userprofile__superior=user)
            ).prefetch_related(Prefetch(
                'members', queryset=get_user_model().objects.select_related('userprofile')
            )).distinct()
        else:
            return Project.objects.filter(
                Q(members=user) | Q(members__isnull=True)
            ).prefetch_related(Prefetch(
                'members', queryset=get_user_model().objects.select_related('userprofile')
            )).distinct()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        projects = self.get_queryset()

        project_filters = ProjectFilters(self.request.GET, queryset=projects)
        projects = project_filters.qs

        data['projects'] = projects
        data['form_filters'] = project_filters.form
        return data


class ProjectDetailView(LoginRequiredMixin, DetailView):
    template_name = 'project/project_details.html'
    model = Project

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(members=user) | Q(members__isnull=True)).prefetch_related(Prefetch(
            'members', queryset=User.objects.select_related('userprofile')))


@method_decorator([manager_required], name='dispatch')
class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'project/update_project.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('projects')


@method_decorator([manager_required], name='dispatch')
class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'project/delete_project.html'
    model = Project
    success_url = reverse_lazy('projects')
