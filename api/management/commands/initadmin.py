from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def create_super_user(self):
        email = settings.ADMIN_EMAIL
        if not email:
            self.stderr.write("No admin email!")
            self.stderr.write("Create admin with default email!")
            admin = "admin@admin.com"
        password = settings.INITIAL_ADMIN_PASSWORD
        if not password:
            self.stderr.write("No admin password!")
            self.stderr.write("Create admin with default password!")
            password = "admin"
        User.objects.create_superuser(
            username="admin",
            email=email,
            password=password
        )
        self.stdout.write("Admin created!")

    def handle(self, *args, **options):
        try:
            User.objects.get(is_superuser=True, is_active=True)
        except User.DoesNotExist:
            self.stdout.write("No admin!")
            self.create_super_user()
        else:
            self.stdout.write("Admin user exists!")
