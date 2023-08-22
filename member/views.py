from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import redirect
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from MyTeam.settings import EMAIL_HOST_USER
from member.forms import MemberSignUpForm, MemberUpdateForm
from userextend.decorators import manager_required
from userextend.models import UserProfile

User = get_user_model()


@method_decorator([manager_required], name='dispatch')
class MemberSignUpView(LoginRequiredMixin, CreateView):
    template_name = 'member/add_member.html'
    form_class = MemberSignUpForm
    success_url = reverse_lazy('add-member')

    def form_valid(self, form):
        form.instance.is_member = True
        user = form.save()
        user.save()

        token_generator = PasswordResetTokenGenerator()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        set_password = self.request.build_absolute_uri(
            reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        )

        details_user = {
            'fullname': f'{user.first_name} {user.last_name}',
            'username': user.username,
            'set_password': set_password
        }
        subject = 'Set Password'
        message = get_template('member_registration_email.html').render(details_user)
        mail = EmailMessage(subject, message, EMAIL_HOST_USER, [user.email])
        mail.content_subtype = 'html'
        mail.send()

        return redirect('members')


class MemberListView(LoginRequiredMixin, ListView):
    template_name = 'member/members.html'
    model = UserProfile
    context_object_name = 'members'

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_queryset(self):
        user_profile = self.get_object()
        logged_in_user = user_profile.user

        if user_profile.user.is_manager:
            members = UserProfile.objects.filter(superior=logged_in_user)
        else:
            members = UserProfile.objects.filter(Q(superior=user_profile.superior) | Q(user=user_profile.superior))

        members |= UserProfile.objects.filter(user=logged_in_user)

        return members.distinct()


@method_decorator([manager_required], name='dispatch')
class MemberDetailView(LoginRequiredMixin, DetailView):
    template_name = 'member/member_profile.html'
    model = UserProfile
    context_object_name = 'profile'


@method_decorator([manager_required], name='dispatch')
class MemberUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'member/update_member_profile.html'
    model = UserProfile
    form_class = MemberUpdateForm
    success_url = reverse_lazy('members')


@method_decorator([manager_required], name='dispatch')
class MemberDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'member/delete_member.html'
    model = User
    context_object_name = 'member'
    success_url = reverse_lazy('members')
