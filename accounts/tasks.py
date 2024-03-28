from celery import shared_task
from django.core.mail import send_mail
from configurations.settings import EMAIL_HOST_USER


@shared_task
def send_email_confirmation(data):
    send_mail(
        subject=data["email_subject"],
        message=data["email_body"],
        from_email=EMAIL_HOST_USER,
        recipient_list=[data["to_email"]]
    )