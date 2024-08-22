from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


# Create your tests here.
class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='test@test.com')
        self.course = Course.objects.create(name='Test course', description='Test description', user=self.user)
        self.lesson = Lesson.objects.create(
            name="test lesson",
            description="test description",
            video_link="https://www.youtube.com/test_video_link",
            course=self.course,
            user=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """Тестирование создания урока"""
        response = self.client.post(
            '/lesson/create/',
            data={
                "name": "test lesson 2",
                "description": "test description 2",
                "video_link": "https://www.youtube.com/test_video_link_2",
                "course": self.course.pk,
                "user": self.user.pk
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {"id": self.lesson.pk + 1,
             "name": "test lesson 2",
             "description": "test description 2",
             "preview": None,
             "video_link": "https://www.youtube.com/test_video_link_2",
             "course": self.course.pk,
             "user": self.user.pk
             }
        )

    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""
        response = self.client.get(
            '/lesson/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {"id": self.lesson.pk,
                     "name": "test lesson",
                     "description": "test description",
                     "preview": None,
                     "video_link": "https://www.youtube.com/test_video_link",
                     "course": self.course.pk,
                     "user": self.user.pk
                     }
                ]
            }
        )

    def test_retrieve_lesson(self):
        """Тестирование вывода одного урока"""
        response = self.client.get(
            reverse('materials:lesson_view', args=(self.lesson.pk,)),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {"id": self.lesson.pk,
             "name": "test lesson",
             "description": "test description",
             "preview": None,
             "video_link": "https://www.youtube.com/test_video_link",
             "course": self.course.pk,
             "user": self.user.pk
             }
        )
        self.assertEqual(
            self.lesson.__str__(),
            'test lesson'
        )

    def test_update_lesson(self):
        """Тестирование изменения урока"""
        response = self.client.patch(
            reverse('materials:lesson_update', args=(self.lesson.pk,)),
            data={"name": "update test lesson",
                  "video_link": "https://www.youtube.com/updated_test_video_link"}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {"id": self.lesson.pk,
             "name": "update test lesson",
             "description": "test description",
             "preview": None,
             "video_link": "https://www.youtube.com/updated_test_video_link",
             "course": self.course.pk,
             "user": self.user.pk
             }
        )

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        response = self.client.delete(
            reverse('materials:lesson_delete', args=(self.lesson.pk,))
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_bad_video_link(self):
        response = self.client.post(
            '/lesson/create/',
            data={
                "name": "test lesson 2",
                "description": "test description 2",
                "video_link": "https://www.not-youtube.com/test_video_link_2",
                "course": self.course.pk,
                "user": self.user.pk
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Ссылка на видео должна быть на сервис youtube.com']}
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='test@test.com')
        self.course = Course.objects.create(name='Test course', description='Test description', user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe_course(self):
        """Тестирование добавления и удаления подписки"""
        response = self.client.post(
            reverse('materials:subscribe_course', args=(self.course.pk,))
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'message': 'подписка добавлена'}
        )
        response = self.client.post(
            reverse('materials:subscribe_course', args=(self.course.pk,))
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'message': 'подписка удалена'}
        )


class CourseTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='test@test.com')
        self.course = Course.objects.create(name='test course', description='test description', user=self.user)
        self.lesson = Lesson.objects.create(
            name="test lesson",
            description="test description",
            video_link="https://www.youtube.com/test_video_link",
            course=self.course,
            user=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        """Тестирование создания курса"""
        response = self.client.post(
            '/course/',
            data={
                "name": "test course 2",
                "description": "test description 2",
                "user": self.user.pk
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {"id": 2,
             "name": "test course 2",
             "description": "test description 2",
             "preview": None,
             "user": self.user.pk
             }
        )

    def test_list_course(self):
        """Тестирование вывода списка курсов"""
        response = self.client.get(
            '/course/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {
                        "id": self.course.pk,
                        'lessons_count': 1,
                        'lessons': [
                            {
                                'id': self.lesson.pk,
                                'name': "test lesson",
                                'description': "test description",
                                'preview': None,
                                'video_link': "https://www.youtube.com/test_video_link",
                                'course': self.course.pk,
                                'user': self.user.pk
                            }
                        ],
                        'is_subscribed': False,
                        "name": "test course",
                        "description": "test description",
                        "preview": None,
                        "user": self.user.pk
                    }
                ]
            }
        )

    def test_retrieve_course(self):
        """Тестирование вывода одного курса"""
        response = self.client.get(
            reverse('materials:course-detail', args=(self.course.pk,)),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                "id": self.course.pk,
                'lessons_count': 1,
                'lessons': [
                    {
                        'id': self.lesson.pk,
                        'name': "test lesson",
                        'description': "test description",
                        'preview': None,
                        'video_link': "https://www.youtube.com/test_video_link",
                        'course': self.course.pk,
                        'user': self.user.pk
                    }
                ],
                'is_subscribed': False,
                "name": "test course",
                "description": "test description",
                "preview": None,
                "user": self.user.pk
            }
        )
        self.assertEqual(
            self.course.__str__(),
            'test course'
        )

    def test_update_course(self):
        """Тестирование изменения курса"""
        response = self.client.patch(
            reverse('materials:course-detail', args=(self.course.pk,)),
            data={"name": "update test course"}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                "id": self.course.pk,
                'lessons_count': 1,
                'lessons': [
                    {
                        'id': self.lesson.pk,
                        'name': "test lesson",
                        'description': "test description",
                        'preview': None,
                        'video_link': "https://www.youtube.com/test_video_link",
                        'course': self.course.pk,
                        'user': self.user.pk
                    }
                ],
                'is_subscribed': False,
                "name": "update test course",
                "description": "test description",
                "preview": None,
                "user": self.user.pk
            }
        )

    def test_delete_course(self):
        """Тестирование удаления курса"""
        response = self.client.delete(
            reverse('materials:course-detail', args=(self.course.pk,))
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
