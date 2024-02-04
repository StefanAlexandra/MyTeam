from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class JobTitle(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    gender_options = [('', '---------'), ('male', 'Male'), ('female', 'Female')]

    birth_date = models.DateField()
    gender = models.CharField(choices=gender_options, max_length=6)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    country = models.CharField(max_length=50)
    county = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=30)
    street_number = models.IntegerField()
    address = models.CharField(max_length=70)
    phone = models.CharField(max_length=30)
    personal_email = models.EmailField(max_length=50)
    start_date = models.DateField()
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    job_description = models.FileField(upload_to='job_descriptions/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    superior = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_age(self):
        today = date.today()
        birth_date = self.birth_date

        years = today.year - birth_date.year
        months = today.month - birth_date.month

        if today.day < birth_date.day:
            months -= 1

        if months < 0:
            years -= 1
            months += 12

        return f'{years} years, {months} months'

    def calculate_time_of_employment(self):
        current_date = date.today()
        start_date = self.start_date

        time_of_employment = current_date - start_date

        years = time_of_employment.days // 365
        months = (time_of_employment.days % 365) // 30

        if current_date > start_date:
            return f'{years} years, {months} months'
        else:
            return '0 years, 0 months'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
