from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from authapp.models import ShopUser


def send_verify_mail(user: ShopUser):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
    subject = 'Account Verify'
    message = f'{settings.BASE_URL}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
