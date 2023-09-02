from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.apps import apps


class Command(BaseCommand):
    name = 'update_fixtures'
    help = 'Update fixtures for all models with integer primary keys to big integers'

    def handle(self, *args, **options):
        # Iterate through all models in all apps
        for model in apps.get_models():
            try:
                app_name = model._meta.app_label
                model_name = model.__name__
                fixture_filename = f"{app_name}/{model_name}_updated.json"

                # Dump the updated fixture for the current model
                call_command('dumpdata', f"{app_name}.{model_name}", '--natural-primary', '--indent', '2', '>', fixture_filename)

                # Load the updated fixture for the current model
                call_command('loaddata', fixture_filename)

                self.stdout.write(self.style.SUCCESS(f"Updated fixture for {app_name}.{model_name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to update fixture for {model}: {e}"))
