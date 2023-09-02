from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class RequestType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class RequestManagement(models.Model):

    status_options = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Declined', 'Declined')]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_maker')
    type = models.ForeignKey(RequestType, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    details = models.TextField(max_length=500)
    status = models.CharField(choices=status_options, max_length=8, default='Pending')
    comments = models.TextField(max_length=500, null=True, blank=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='requests_approver')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # If the requester has a superior, set the manager field to the superior
        if self.requester and self.requester.userprofile.superior:
            self.manager = self.requester.userprofile.superior

        super(RequestManagement, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.requester} - {self.type} - {self.created_at.date()}'
