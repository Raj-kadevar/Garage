from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_email(request, user):
    mail_subject = 'Email Verification.'
    # breakpoint()
    message = render_to_string('email_verify.html', {
        'user': user,
        'domain': request._current_scheme_host,
        'email_sender': settings.EMAIL_SENDER,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'email_title': settings.EMAIL_TITLE,
        'email_contact': settings.EMAIL_CONTACT_INFORMATION,
        'support_mail': settings.SUPPORT_EMAIL_OR_PHONE_NUMBER,
        'validation_period': settings.EMAIL_LINK_VALIDATION_HOURS
    })
    email = EmailMessage(
        subject=mail_subject, body=message, from_email=settings.EMAIL_SENDER, to=[user.email]
    )
    email.send()