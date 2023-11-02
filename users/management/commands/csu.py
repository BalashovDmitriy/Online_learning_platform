from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin@admin.admin",
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        user.set_password("admin")
        user.save()
        self.stdout.write(
            self.style.SUCCESS(f"Created admin {user.email}")
        )
