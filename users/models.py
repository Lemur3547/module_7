from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {'null': True, 'blank': True}
# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=30, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateTimeField(verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    summ = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(choices=[('cash', 'Наличные'), ('cashless', 'Безнал')])

    def __str__(self):
        return f'{self.user} - {self.date}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
