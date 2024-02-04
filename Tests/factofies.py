import factory
from factory import SubFactory, LazyFunction

from userextend.models import Department, JobTitle, User, UserProfile


class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department

    name = 'IT'


class JobTitleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobTitle

    title = 'Junior Developer'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'testpass')
    email = factory.Faker('email')
    is_superuser = False
    is_manager = True
    is_member = False


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = SubFactory(UserFactory)
    birth_date = factory.Faker('date_of_birth')
    gender = factory.Faker('random_element', elements=['male', 'female'])
    country = factory.Faker('country')
    county = factory.Faker('state')
    city = factory.Faker('city')
    street = factory.Faker('street_name')
    street_number = factory.Faker('building_number')
    address = factory.Faker('address')
    phone = factory.Faker('phone_number')
    personal_email = factory.Faker('email')
    start_date = factory.Faker('date_this_decade')
    job_title = SubFactory(JobTitleFactory)
    department = SubFactory(DepartmentFactory)
    superior = LazyFunction(lambda: User.objects.filter(is_manager=True).first())
