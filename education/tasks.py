import datetime

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_user_last_login():
    print("check_user_last_login")
    now = datetime.datetime.now()
    now = timezone.make_aware(now, timezone.get_current_timezone())
    for user in User.objects.all():
        print(f"{user} - {user.last_login}")
        if user.last_login:
            print(now - user.last_login)
            if now - user.last_login > datetime.timedelta(days=30):
                user.is_active = False
                user.save()
