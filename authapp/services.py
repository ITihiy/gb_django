from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from authapp.models import ShopUser, ShopUserProfile
from django.dispatch import receiver
from django.db.models.signals import post_save


def send_verify_mail(user: ShopUser):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
    subject = 'Account Verify'
    message = f'{settings.BASE_URL}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


@receiver(post_save, sender=ShopUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ShopUserProfile.objects.create(user=instance)


@receiver(post_save, sender=ShopUser)
def save_user_profile(sender, instance, **kwargs):
    instance.shopuserprofile.save()
