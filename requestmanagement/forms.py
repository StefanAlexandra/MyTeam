from django import forms
from requestmanagement.models import RequestManagement


class RequestManagementForm(forms.ModelForm):
    class Meta:
        model = RequestManagement
        fields = ['type', 'start_date', 'end_date', 'details']

        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
        }


class RequestManagementUpdateForm(forms.ModelForm):

    class Meta:
        model = RequestManagement
        fields = ['type', 'start_date', 'end_date', 'details', 'status', 'comments']

        widgets = {
            'type': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'start_date': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'end_date': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'details': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'status': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'comments': forms.Textarea(attrs={'class': 'form-control'})
        }
