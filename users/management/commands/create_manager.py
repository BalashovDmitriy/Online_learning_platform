from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="manager@manager.ru",
            is_active=True,
            is_staff=True
        )
        user.set_password("manager")
        user.save()
        self.stdout.write(
            self.style.SUCCESS(f"Created manager {user.email}")
        )
