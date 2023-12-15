from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a test user'

    def handle(self, **kwargs):
        username = 'test'
        password = 'test123'

        User.objects.create_user(username, password)

        self.stdout.write(self.style.SUCCESS(f'Test user "{username}" created successfully.'))