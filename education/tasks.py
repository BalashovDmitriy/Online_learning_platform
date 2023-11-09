from celery import shared_task
from django.core.mail import send_mail

from config import settings
from education.models import Subscription


@shared_task
def subscriptions_update_course_mailing(course_id):
    for subscription in Subscription.objects.filter(course_id=course_id):
        send_mail(
            subject='Обновление курса',
            message=f'Курс "{subscription.course}" был обновлен.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscription.user.email],
        )


@shared_task
def test_task(course_id):
    print('test task')
    print(course_id)
