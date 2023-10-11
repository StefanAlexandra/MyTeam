from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from userextend.models import Department, JobTitle, UserProfile

User = get_user_model()


class ModelStringRepresentationTest(TestCase):
    def test_department_str(self):
        department = Department.objects.create(name='HR')
        self.assertEqual(str(department), 'HR')

    def test_jobtitle_str(self):
        job_title = JobTitle.objects.create(title='Junior Software Developer')
        self.assertEqual(str(job_title), 'Junior Software Developer')

    def test_user_str(self):
        user = User.objects.create(first_name='Liz', last_name='Jones')
        self.assertEqual(str(user), 'Liz Jones')


class UserProfileCalculateAgeTest(TestCase):
    def test_calculate_age_future_birth_date(self):
        # Test when birth date is in the future (should return "0 years, 0 months")
        future_birth_date = date.today() + timedelta(days=365)  # Set birth date to one year in the future
        user_profile = UserProfile(birth_date=future_birth_date)
        self.assertEqual(user_profile.calculate_age(), "0 years, 0 months")

    def test_calculate_age_same_month_and_day(self):
        # Test when birth date is in the same month and day as today (should return "0 years, 0 months")
        today = date.today()
        user_profile = UserProfile(birth_date=today)
        self.assertEqual(user_profile.calculate_age(), "0 years, 0 months")

    def test_calculate_age_past_birth_date(self):
        # Test when birth date is in the past (should return the correct age)
        past_birth_date = date.today() - timedelta(days=365*30)  # Set birth date to 30 years ago
        user_profile = UserProfile(birth_date=past_birth_date)
        expected_age = f"{30} years, 0 months"  # 30 years, 0 months
        self.assertEqual(user_profile.calculate_age(), expected_age)

    def test_calculate_age_partial_month(self):
        # Test when birth date is in the past, but the current month is not yet completed (should handle partial months)
        today = date.today()
        birth_date = today.replace(year=today.year - 1, month=today.month - 3)  # 9 months ago
        user_profile = UserProfile(birth_date=birth_date)
        expected_age = f"{0} years, {9} months"  # 0 years, 9 months
        self.assertEqual(user_profile.calculate_age(), expected_age)

    def test_calculate_age_partial_day(self):
        # Test when birth date is in the past, but the current day is not yet completed (should handle partial days)
        today = date.today()
        birth_date = today.replace(year=today.year - 1, month=today.month, day=today.day - 5)  # 360 days ago
        user_profile = UserProfile(birth_date=birth_date)
        expected_age = f"{0} years, {11} months"  # 0 years, 11 months
        self.assertEqual(user_profile.calculate_age(), expected_age)
