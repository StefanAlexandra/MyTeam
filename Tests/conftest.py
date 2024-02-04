import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyTeam.settings")
django.setup()


from pytest_factoryboy import register
from Tests.factofies import DepartmentFactory, JobTitleFactory, UserProfileFactory, UserFactory


register(DepartmentFactory)
register(JobTitleFactory)
register(UserFactory)
register(UserProfileFactory)
