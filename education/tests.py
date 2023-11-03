from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from education.models import Course, Lesson
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
        self.assertEqual(response.status_code, 200)
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
