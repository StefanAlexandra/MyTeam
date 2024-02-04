from datetime import date
import mock
import pytest

pytestmark = pytest.mark.django_db


def test_department_model_str_return(department_factory):
    department = department_factory(name='it')
    assert department.__str__() == 'it'


def test_job_title_model_str_return(job_title_factory):
    job_title = job_title_factory(title='Junior Developer')
    assert job_title.__str__() == 'Junior Developer'


def test_user_model_str_return(user_factory):
    user = user_factory(first_name='Jhon', last_name='Doe')
    assert user.__str__() == 'Jhon Doe'


class TestUserProfile:
    def test_user_profile_model_str_return(self, user_profile_factory):
        user_profile = user_profile_factory(user__first_name='Jhon', user__last_name='Done')
        assert user_profile.__str__() == 'Jhon Done'

    def test_calculate_age(self, user_profile_factory):
        case_1 = user_profile_factory(birth_date=date(1994, 8, 29))
        case_2 = user_profile_factory(birth_date=date(1994, 2, 1))
        case_3 = user_profile_factory(birth_date=date(1994, 1, 1))
        with mock.patch('django.utils.timezone.now', return_value=date(2024, 2, 4)):
            assert case_1.calculate_age() == "29 years, 5 months"
            assert case_2.calculate_age() == "30 years, 0 months"
            assert case_3.calculate_age() == "30 years, 1 months"

    def test_calculate_time_of_employment(self, user_profile_factory):
        user_profile = user_profile_factory(start_date=date(2023, 9, 1))
        with mock.patch('django.utils.timezone.now', return_value=date(2024, 2, 4)):
            assert user_profile.calculate_time_of_employment() == '0 years, 5 months'

