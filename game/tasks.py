from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail


@shared_task
def send_mail_to_all(subject, plain_message, html_message, from_email=settings.DEFAULT_FROM_EMAIL):
    receivers = []
    for user in User.objects.all():
        receivers.append(user.email)

    send_mail(subject, plain_message, from_email, receivers, html_message=html_message, fail_silently=False)


@shared_task
def send_something_to_me():
    subject = "Cześć"
    plain_message = "O super, zadziałało!"
    from_email = settings.DEFAULT_FROM_EMAIL
    receivers = [settings.ADMIN_EMAIL, ]
    send_mail(subject, plain_message, from_email, receivers, fail_silently=False)
