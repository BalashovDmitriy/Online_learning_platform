import stripe
from django.core.mail import send_mail

from config import settings
from education.models import Subscription, Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


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


def get_session(serializer: Payment):
    """ Получает сессию для оплаты курса """
    course_title = serializer.course.title
    product = stripe.Product.create(name=course_title)
    price = stripe.Price.create(
        unit_amount=serializer.course.price * 100,
        currency='rub',
        product=product.id,
    )
    session = stripe.checkout.Session.create(
        success_url='https://example.com/success',
        line_items=[
            {
                'price': price.id,
                'quantity': 1,
            }
        ],
        mode='payment',
        customer_email=serializer.user.email
    )
    send_payment_link_to_mail(session.url, serializer.user.email)
    return session


def retrieve_session(session):
    """ Получаем детали сессии"""
    return stripe.checkout.Session.retrieve(session)


def send_payment_link_to_mail(url, email):
    send_mail(
        subject='Оплата курса',
        message=f'Ссылка для оплаты курса: {url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )
