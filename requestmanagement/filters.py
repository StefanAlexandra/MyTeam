import django_filters
from requestmanagement.models import RequestManagement


class RequestManagementFilters(django_filters.FilterSet):
    class Meta:
        model = RequestManagement
        fields = ['type', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['type'].field.widget.attrs.update({'class': 'form-control'})
        self.filters['status'].field.widget.attrs.update({'class': 'form-control'})


