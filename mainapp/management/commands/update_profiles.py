from django.core.management import BaseCommand

from authapp.models import ShopUser, ShopUserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in ShopUser.objects.filter(shopuserprofile=None):
            ShopUserProfile.objects.create(user=user)
