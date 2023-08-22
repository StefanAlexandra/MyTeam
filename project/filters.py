import django_filters
from django import forms
from project.models import Project


class ProjectFilters(django_filters.FilterSet):

    project_title = django_filters.CharFilter(lookup_expr='icontains', label='Project')
    planned_start_gte = django_filters.DateFilter(field_name='planned_start', lookup_expr='gte', label='From',
                                                  widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    planned_start_lte = django_filters.DateFilter(field_name='planned_start', lookup_expr='lte', label='To',
                                                  widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    planned_end_gte = django_filters.DateFilter(field_name='planned_end', lookup_expr='gte', label='From',
                                                widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    planned_end_lte = django_filters.DateFilter(field_name='planned_end', lookup_expr='lte', label='To',
                                                widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Project
        fields = ['project_title', 'planned_start_gte', 'planned_start_lte', 'planned_end_gte', 'planned_end_lte',
                  'status', 'priority']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['project_title'].field.widget.attrs.update({'class': 'form-control'})
        self.filters['status'].field.widget.attrs.update({'class': 'form-control'})
        self.filters['priority'].field.widget.attrs.update({'class': 'form-control'})
