from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from requestmanagement.filters import RequestManagementFilters
from requestmanagement.forms import RequestManagementForm, RequestManagementUpdateForm
from requestmanagement.models import RequestManagement
from userextend.decorators import member_required

User = get_user_model()


@method_decorator([member_required], name='dispatch')
class RequestManagementCreateView(LoginRequiredMixin, CreateView):
    template_name = 'requestmanagement/make_request.html'
    model = RequestManagement
    form_class = RequestManagementForm
    success_url = reverse_lazy('requests-list')

    def form_valid(self, form):
        form.instance.requester = self.request.user
        return super().form_valid(form)


class RequestManagementListView(LoginRequiredMixin, ListView):
    template_name = 'requestmanagement/requersts.html'
    model = RequestManagement
    context_object_name = 'requests_list'

    def get_queryset(self):
        user = self.request.user

        if user.is_manager:
            return RequestManagement.objects.filter(manager=user).prefetch_related(
                Prefetch('manager', queryset=User.objects.select_related('userprofile')))
        elif user.is_member:
            return RequestManagement.objects.filter(requester=user).prefetch_related(
                Prefetch('requester', queryset=User.objects.select_related('userprofile')))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        requests_list = self.get_queryset()

        requests_filters = RequestManagementFilters(self.request.GET, queryset=requests_list)
        requests_list = requests_filters.qs

        data['requests_list'] = requests_list
        data['form_filters'] = requests_filters.form
        return data


class RequestManagementDetailView(LoginRequiredMixin, DetailView):
    template_name = 'requestmanagement/request_details.html'
    model = RequestManagement
    context_object_name = 'request'


class RequestManagementUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'requestmanagement/update_request.html'
    model = RequestManagement
    success_url = reverse_lazy('requests-list')

    def get_form_class(self):
        user = self.request.user

        if user.is_manager:
            return RequestManagementUpdateForm
        elif user.is_member:
            return RequestManagementForm

    def form_valid(self, form):
        user = self.request.user
        if user.is_manager:
            instance = form.save(commit=False)

            if 'approve' in self.request.POST:
                instance.status = 'Approved'
            elif 'decline' in self.request.POST:
                instance.status = 'Declined'

            instance.save()
            return super().form_valid(form)


@method_decorator([member_required], name='dispatch')
class RequestManagementDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'requestmanagement/delete_request.html'
    model = RequestManagement
    context_object_name = 'request'
    success_url = reverse_lazy('requests-list')
