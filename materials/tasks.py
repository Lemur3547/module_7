import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from materials.models import Subscription
from users.models import User


@shared_task
def update_course_email(course):
    subscriptions = Subscription.objects.filter(course=course)
    user_list = [subs.user.email for subs in subscriptions]
    send_mail(
        subject='Обновление курса!',
        message=f'Для курса {course.name} вышло обновление. Зайдите и посмотрите сейчас!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=user_list,
        fail_silently=True
    )


@shared_task
def check_user_activity():
    users = User.objects.filter(is_active=True)
    today = datetime.date.today()
    for user in users:
        if user.last_login:
            if today - user.last_login.date() > datetime.timedelta(days=30):
                user.is_active = False
                user.save()
        else:
            if today - user.date_joined.date() > datetime.timedelta(days=30):
                user.is_active = False
                user.save()
