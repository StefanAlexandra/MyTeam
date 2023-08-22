from django import forms
from userextend.models import UserProfile


class UserProfileUpdateForm(forms.ModelForm):
    # Add the user's first_name and last_name fields
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'birth_date', 'gender',
                  'country', 'county', 'city', 'street', 'street_number', 'address', 'phone', 'personal_email']

    def save(self, commit=True):
        # Save the UserProfile instance
        profile = super().save(commit=False)

        # Update the related User instance
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if self.cleaned_data['profile_picture']:
            profile.profile_picture = self.cleaned_data['profile_picture']

        if commit:
            user.save()
            profile.save()

        return profile
