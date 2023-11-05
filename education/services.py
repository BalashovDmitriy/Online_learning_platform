from django.core.mail import send_mail

from config import settings
from education.models import Subscription


def subscriptions_update_course_mailing(serializer):
    for subscription in Subscription.objects.filter(course_id=serializer.instance.id):
        send_mail(
            subject='Обновление курса',
            message=f'Курс "{serializer.instance}" был обновлен.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscription.user.email],
        )


def subscriptions_lesson_mailing(serializer):
    for subscription in Subscription.objects.filter(course_id=serializer.instance.course.id):
        send_mail(
            subject='Обновление урока',
            message=f'{serializer.instance} был обновлен.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscription.user.email],
        )


def subscriptions_create_lesson_mailing(serializer):
    for subscription in Subscription.objects.filter(course_id=serializer.instance.course.id):
        send_mail(
            subject='Добавление урока',
            message=f'{serializer.instance} был добавлен.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscription.user.email],
        )
