from django.contrib.auth import get_user_model
from django.db import models
from project.models import Project

User = get_user_model()


class Task(models.Model):

    status_options = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Blocked', 'Blocked'),
        ('Done', 'Done'),
    ]

    priority_options = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    title = models.CharField(max_length=100)
    related_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    estimated_hours = models.IntegerField()
    status = models.CharField(choices=status_options, max_length=11, default='Open')
    priority = models.CharField(choices=priority_options, max_length=6)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_staff': False})

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'Done':
            project = self.related_project
            project.completion = project.completion()
            project.save()

    def completion(self):
        total_tasks = self.related_project.task_set.count()
        done_tasks = self.related_project.task_set.filter(status='Done').count()

        if total_tasks > 0:
            completion = round(done_tasks / total_tasks * 100)
        else:
            completion = 0

        return completion
