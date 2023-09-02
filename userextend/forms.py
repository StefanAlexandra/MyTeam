from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, \
    SetPasswordForm
from django.core.validators import validate_email
from django.db import transaction
from userextend.models import UserProfile, JobTitle, Department

User = get_user_model()


class AuthenticationNewForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Please enter username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Please enter password'})


class PasswordResetNewForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Please enter your email'})


class SetPasswordNewForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter password'})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please confirm your password'})


class BaseSignUpForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=UserProfile.gender_options,
                               initial=None)
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    county = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    street = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    street_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    personal_email = forms.EmailField(validators=[validate_email],
                                      widget=forms.EmailInput(attrs={'class': 'form-control'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    job_title = forms.ModelChoiceField(queryset=JobTitle.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    job_description = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    resume = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    superior = forms.ModelChoiceField(queryset=User.objects.filter(is_manager=True), required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()

        cleaned_data['first_name'] = cleaned_data['first_name'].title()
        cleaned_data['last_name'] = cleaned_data['last_name'].title()
        cleaned_data['country'] = cleaned_data['country'].title()
        cleaned_data['county'] = cleaned_data['county'].title()
        cleaned_data['city'] = cleaned_data['city'].title()
        cleaned_data['street'] = cleaned_data['street'].title()
        cleaned_data['address'] = cleaned_data['address'].title()
        cleaned_data['personal_email'] = cleaned_data['personal_email'].lower()

        return cleaned_data


class ManagerSignUpForm(UserCreationForm, BaseSignUpForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})

    @transaction.atomic
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.is_manager = True
        if commit:
            user.save()
            profile_data = {
                key: value for key, value in self.cleaned_data.items()
                if key not in ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
            }
            profile = UserProfile.objects.create(user=user, **profile_data)
        return user


class PasswordChangeNewForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your old password'})
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your new password'})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please confirm your new password'})
