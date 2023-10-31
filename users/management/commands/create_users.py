from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="reaver_std@mail.ru",
            is_active=True,
        )
        user.set_password("598420")
        user.save()
        self.stdout.write(
            self.style.SUCCESS(f"Created user {user.email}")
        )
        user = User.objects.create(
            email="reaver74@yandex.ru",
            is_active=True,
        )
        user.set_password("598420")
        user.save()
        self.stdout.write(
            self.style.SUCCESS(f"Created user {user.email}")
        )
