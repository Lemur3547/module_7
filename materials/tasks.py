from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def update_course_email(course, users_list):
    send_mail(
        subject='Обновление курса!',
        message=f'Для курса {course} вышло обновление. Зайдите и посмотрите сейчас!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=users_list,
        fail_silently=True
    )
