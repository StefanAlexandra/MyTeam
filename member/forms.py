from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from userextend.forms import BaseSignUpForm
from userextend.models import UserProfile, JobTitle, Department

User = get_user_model()


class MemberSignUpForm(BaseSignUpForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control'})

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_member = True
        group = Group.objects.get(name='Members')
        random_password = User.objects.make_random_password()
        user.set_password(random_password)
        if commit:
            user.save()
            user.groups.add(group)
            profile_data = {
                key: value for key, value in self.cleaned_data.items()
                if key not in ['username', 'email', 'password', 'first_name', 'last_name']
            }
            profile = UserProfile.objects.create(user=user, **profile_data)
        return user


class MemberUpdateForm(forms.ModelForm):

    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(max_length=150, required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['superior'].queryset = User.objects.filter(is_manager=True)
            self.fields['job_title'].queryset = JobTitle.objects.all()
            self.fields['department'].queryset = Department.objects.all()

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'birth_date', 'gender', 'country', 'county', 'city',
                  'street', 'street_number', 'address', 'phone', 'personal_email',
                  'job_title', 'department', 'job_description', 'resume', 'superior']

    def save(self, commit=True):
        profile = super().save(commit=False)

        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if self.cleaned_data['profile_picture']:
            user.userprofile.profile_picture = self.cleaned_data['profile_picture']

        if commit:
            user.save()
            profile.save()

        return profile
