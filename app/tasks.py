
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.core.management import call_command



@shared_task
def call_statistics_command(*args, **kwargs):
    call_command("make_statistics", *args, **kwargs)


@shared_task
def send_html_email(subject, html_content, recipient_list):
    message = EmailMessage(
        subject, html_content, settings.DEFAULT_FROM_EMAIL, recipient_list
    )
    message.mixed_subtype = "related"
    message.content_subtype = "html"
    message.send()


@shared_task
def backup_database(*args, **kwargs):
    call_command("dbbackup", *args, **kwargs)


@shared_task
def send_email(*, subject, message, from_email=None, recipient_list):
    send_mail(subject, message, from_email, recipient_list)
