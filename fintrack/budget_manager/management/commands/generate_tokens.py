from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = "Generate access tokens for all users"

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            token, created = Token.objects.get_or_create(user=user)
            if created:
                self.stdout.write(f"Token generated for user: {user.username}")
            else:
                self.stdout.write(f"Token already exists for user: {user.username}")
