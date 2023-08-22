from django import forms
from project.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_title', 'project_type', 'project_description', 'status',
                  'complexity', 'priority', 'planned_start', 'planned_end', 'members']

        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'form-control'}),
            'project_type': forms.Select(attrs={'class': 'form-control'}),
            'project_description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'complexity': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'planned_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'planned_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'members': forms.CheckboxSelectMultiple(),
        }
