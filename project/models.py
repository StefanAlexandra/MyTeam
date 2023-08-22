from django.contrib.auth import get_user_model
from django.db import models
from userextend.models import User


class ProjectType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class Project(models.Model):

    status_options = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Blocked', 'Blocked'),
        ('Done', 'Done'),
    ]

    complexity_options = [
        ('Basic', 'Basic'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    priority_options = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    project_title = models.CharField(max_length=150)
    project_type = models.ForeignKey(ProjectType, on_delete=models.SET_NULL, null=True)
    project_description = models.TextField(max_length=500)
    planned_start = models.DateField(blank=True)
    planned_end = models.DateField(blank=True)
    status = models.CharField(choices=status_options, max_length=11, default='Open')
    complexity = models.CharField(choices=complexity_options, max_length=14)
    priority = models.CharField(choices=priority_options, max_length=6)

    members = models.ManyToManyField(get_user_model(), limit_choices_to={'is_staff': False})

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def completion(self):
        total_tasks = self.task_set.count()
        done_tasks = self.task_set.filter(status='Done').count()

        if total_tasks > 0:
            completion = round(done_tasks / total_tasks * 100)
        else:
            completion = 0

        return completion

    def __str__(self):
        return self.project_title
