from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from userextend.models import UserProfile
from userprofile.forms import UserProfileUpdateForm


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'userprofile/user_profile.html'
    model = UserProfile
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.userprofile


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'userprofile/update_user_profile.html'
    form_class = UserProfileUpdateForm

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('user-profile', kwargs={'pk': pk})
