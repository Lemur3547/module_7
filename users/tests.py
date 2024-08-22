import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course
from users.models import User, Payment


# Create your tests here.


class RegisterTestCase(APITestCase):
    def test_create_user(self):
        """Тестирование создания пользователя"""
        response = self.client.post(
            '/users/register/',
            data={
                'email': 'newtest@test.com',
                'password': 'testpassword'
            }
        )
        newuser = User.objects.get(email='newtest@test.com')
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {
                "id": newuser.id,
                "password": newuser.password,
                "last_login": None,
                "is_superuser": False,
                "first_name": "",
                "last_name": "",
                "is_staff": False,
                "is_active": False,
                "date_joined": newuser.date_joined.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "email": "newtest@test.com",
                "phone": None,
                "city": None,
                "avatar": None,
                "groups": [],
                "user_permissions": []
            }
        )


class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.another_user = User.objects.create(email='another@email.com')
        self.client.force_authenticate(user=self.user)

    def test_user_list(self):
        """Тестирование вывода списка пользователей"""
        response = self.client.get(
            '/users/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            [
                {
                    "id": self.user.pk,
                    "email": "test@test.com",
                    "phone": None,
                    "city": None,
                    "avatar": None
                },
                {
                    "id": self.another_user.pk,
                    "email": "another@email.com",
                    "phone": None,
                    "city": None,
                    "avatar": None
                },
            ]
        )

    def test_self_user_detail(self):
        """Тестирование вывода одного текущего пользователя"""
        response = self.client.get(
            reverse('users:view_user', args=(self.user.pk,)),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                "id": self.user.id,
                "password": self.user.password,
                "last_login": None,
                "is_superuser": False,
                "first_name": "",
                "last_name": "",
                "is_staff": False,
                "is_active": True,
                "date_joined": self.user.date_joined.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "email": "test@test.com",
                "phone": None,
                "city": None,
                "avatar": None,
                'payments': [],
                "groups": [],
                "user_permissions": []
            }
        )
        self.assertEqual(
            self.user.__str__(),
            'test@test.com'
        )

    def test_another_user_detail(self):
        """Тестирование вывода одного другого пользователя"""
        response = self.client.get(
            reverse('users:view_user', args=(self.another_user.pk,)),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                "id": self.another_user.pk,
                "email": "another@email.com",
                "phone": None,
                "city": None,
                "avatar": None
            }
        )

    def test_update_user(self):
        """Тестирование изменения пользователя"""
        response = self.client.patch(
            reverse('users:update_user', args=(self.user.pk,)),
            data={
                'email': 'updatedmail@email.com'
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()["email"],
            'updatedmail@email.com'
        )

    def test_delete_user(self):
        """Тестирование удаления пользователя"""
        response = self.client.delete(
            reverse('users:delete_user', args=(self.user.pk,))
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class PaymentTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.course = Course.objects.create(name='Test course', description='Test description', user=self.user)
        self.payment = Payment.objects.create(
            user=self.user,
            date=datetime.datetime(2024, 8, 22, 16, 45, 4),
            course=self.course,
            summ=12990,
            payment_method='cashless'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_payment(self):
        """Тестирование создания платежа"""
        response = self.client.post(
            '/payment/',
            data={
                "user": self.user.pk,
                "date": '2012-04-23T18:25:43.511123Z',
                "course": self.course.pk,
                "summ": 16500,
                "payment_method": 'cash'
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {
                "id": self.payment.pk + 1,
                "user": self.user.pk,
                "date": '2012-04-23T18:25:43.511123Z',
                "course": self.course.pk,
                "lesson": None,
                "summ": 16500,
                "payment_method": 'cash'
            }
        )

    def test_list_payment(self):
        """Тестирование вывода списка платежей"""
        response = self.client.get(
            '/payment/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            [
                {
                    "id": self.payment.pk,
                    "user": self.user.pk,
                    "date": '2024-08-22T16:45:04Z',
                    "course": self.course.pk,
                    "lesson": None,
                    "summ": 12990,
                    "payment_method": 'cashless'
                }
            ]
        )

    def test_detail_payment(self):
        """Тестирование вывода одного платежа"""
        response = self.client.get(
            reverse('materials:payment-detail', args=(self.payment.pk,))
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                "id": self.payment.pk,
                "user": self.user.pk,
                "date": '2024-08-22T16:45:04Z',
                "course": self.course.pk,
                "lesson": None,
                "summ": 12990,
                "payment_method": 'cashless'
            }
        )
        self.assertEqual(
            self.payment.__str__(),
            'test@test.com - 2024-08-22 16:45:04'
        )

    def test_update_payment(self):
        """Тестирование изменения платежа"""
        response = self.client.patch(
            reverse('materials:payment-detail', args=(self.payment.pk,)),
            data={
                "summ": 14500,
                "payment_method": 'cash'
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                "id": self.payment.pk,
                "user": self.user.pk,
                "date": '2024-08-22T16:45:04Z',
                "course": self.course.pk,
                "lesson": None,
                "summ": 14500,
                "payment_method": 'cash'
            }
        )

    def test_delete_payment(self):
        """Тестирование удаления платежа"""
        response = self.client.delete(
            reverse('materials:payment-detail', args=(self.payment.pk,))
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
