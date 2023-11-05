import pytz
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from config import settings
from education.models import Course, Lesson, Subscription, Payment
from users.models import User


class LessonsAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.test', is_active=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Тестовый курс')
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            description='Тестовое описание',
            course=self.course,
            owner=self.user,
        )

    def test_lesson_list(self):
        """ Проверка списка уроков """
        response = self.client.get(reverse('lesson-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'count': 1,
                          'next': None,
                          'previous': None,
                          'results': [
                              {'id': self.lesson.id,
                               'title': self.lesson.title,
                               'description': self.lesson.description,
                               'image': self.lesson.image,
                               'link': self.lesson.link,
                               'course': self.lesson.course.title,
                               }
                          ]
                          }
                         )

    def test_lesson_retrieve(self):
        """ Проверка получения урока """
        response = self.client.get(reverse('lesson-retrieve', args=[self.lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'id': self.lesson.id,
                          'title': self.lesson.title,
                          'description': self.lesson.description,
                          'image': self.lesson.image,
                          'link': self.lesson.link,
                          'course': self.lesson.course.title,
                          }
                         )

    def test_lesson_create(self):
        """ Проверка создания урока """
        data = {
            'title': 'Тестовый урок 2',
            'description': 'Тестовое описание 2',
            'course': self.course,
            'link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        }
        response = self.client.post(reverse('lesson-create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_create_link_validation(self):
        """ Проверка валидации ссылки на видео """
        data = {
            'title': 'Тестовый урок 3',
            'description': 'Тестовое описание 3',
            'course': self.course,
            'link': 'https://www.some.com/watch?v=dQw4w9WgXcQ',
        }
        response = self.client.post(reverse('lesson-create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Ссылка на видео должна быть на youtube.com']})

    def test_lesson_update(self):
        """ Проверка обновления урока """
        data = {
            'title': 'Тестовый урок тест на изменение',
            'description': 'Тестовое описание тест на изменение',
            'course': self.course,
        }
        response = self.client.put(reverse('lesson-update', args=[self.lesson.id]), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'id': self.lesson.id,
                          'title': data['title'],
                          'description': data['description'],
                          'image': self.lesson.image,
                          'link': self.lesson.link,
                          'course': self.lesson.course.title,
                          }
                         )

    def test_lesson_delete(self):
        """ Проверка удаления урока """
        response = self.client.delete(reverse('lesson-delete', args=[self.lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.test', is_active=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Тестовый курс')
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            description='Тестовое описание',
            course=self.course,
            owner=self.user,
        )
        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
        )

    def test_subscription_list(self):
        """ Проверка списка подписок """
        response = self.client.get(reverse('subscription-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         [
                             {'id': self.subscription.id,
                              'user': self.subscription.user.email,
                              'course': self.subscription.course.title,
                              }
                         ])

    def test_subscription_delete(self):
        """ Проверка удаления подписки """
        response = self.client.delete(reverse('subscription-delete', args=[self.subscription.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 0)


class CoursesAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.test', is_active=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Тестовый курс', owner=self.user)

    def test_course_list(self):
        """ Проверка списка курсов """
        response = self.client.get('/course/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'count': 1,
                          'next': None,
                          'previous': None,
                          'results': [
                              {'id': self.course.id,
                               'lessons_count': self.course.lessons.count(),
                               'lessons': [],
                               'course_subscription': False,
                               'title': self.course.title,
                               'description': self.course.description,
                               'image': self.course.image,
                               'owner': self.course.owner.id}
                          ]
                          }
                         )

    def test_course_retrieve(self):
        """ Проверка получения курса """
        response = self.client.get(f'/course/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'id': self.course.id,
                          'lessons_count': self.course.lessons.count(),
                          'lessons': [],
                          'course_subscription': False,
                          'title': self.course.title,
                          'description': self.course.description,
                          'image': self.course.image,
                          'owner': self.course.owner.id,
                          }
                         )

    def test_course_create(self):
        """ Проверка создания курса """
        data = {
            'title': 'Тестовый курс 2',
            'description': 'Тестовое описание 2',
            'owner': self.user,
        }
        response = self.client.post('/course/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_course_update(self):
        """ Проверка обновления курса """
        data = {
            'title': 'Тестовый курс тест на изменение',
            'description': 'Тестовое описание тест на изменение',
            'owner': self.user,
        }
        response = self.client.put(f'/course/{self.course.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'id': self.course.id,
                          'lessons_count': self.course.lessons.count(),
                          'lessons': [],
                          'course_subscription': False,
                          'title': data['title'],
                          'description': data['description'],
                          'image': self.course.image,
                          'owner': self.course.owner.id,
                          }
                         )

    def test_course_delete(self):
        """ Проверка удаления курса """
        response = self.client.delete(f'/course/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


class PaymentAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.test', is_active=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Тестовый курс', owner=self.user)
        self.payment = Payment.objects.create(
            user=self.user,
            course=self.course,
            payment_sum=4500,
            payment_method='1',
        )

    def test_payment_list(self):
        """ Проверка списка оплат """
        response = self.client.get(reverse('payment-list'))
        print(response.json())
        tz = pytz.timezone(settings.TIME_ZONE)
        self.payment.payment_date = self.payment.payment_date.astimezone(tz)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         [
                             {'user': self.payment.user.id,
                              'course': self.payment.course.id,
                              'payment_date': self.payment.payment_date.isoformat(),
                              'payment_sum': self.payment.payment_sum,
                              'payment_method': self.payment.payment_method
                              }
                         ])
