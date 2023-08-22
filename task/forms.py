from django import forms
from task.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'related_project', 'description', 'estimated_hours', 'status',
                  'priority', 'assigned_to']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'related_project': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'estimated_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'})
        }


class TaskStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'related_project', 'description', 'estimated_hours', 'status',
                  'priority', 'assigned_to']

        widgets = {
            'title': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'related_project': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'description': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'estimated_hours': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'assigned_to': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
        }

