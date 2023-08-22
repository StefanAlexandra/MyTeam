import django_filters
from django import forms

from task.models import Task


class TaskFilters(django_filters.FilterSet):

    title = django_filters.CharFilter(lookup_expr='icontains', label='Task')
    created_at_gte = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label='Created From',
                                               widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    created_at_lte = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', label='Created To',
                                               widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Task
        fields = ['title', 'status', 'priority', 'related_project', 'assigned_to', 'created_at_gte', 'created_at_lte']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['title'].field.widget.attrs.update({'class': 'form-control'})
        self.filters['status'].field.widget.attrs.update({'class': 'form-control'})
        self.filters['priority'].field.widget.attrs.update({'class': 'form-control'})
        self.filters['related_project'].field.widget.attrs.update({'class': 'form-control'})
        self.filters['assigned_to'].field.widget.attrs.update({'class': 'form-control'})

