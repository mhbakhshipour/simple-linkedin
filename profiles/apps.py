from django.apps import AppConfig
from django.db.models.signals import post_save
from django.conf import settings


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        from .models import Profile

        def create_profile(sender, instance, created, **kwargs):
            if created:
                Profile.objects.create(user=instance)

        post_save.connect(
            create_profile,
            sender=settings.AUTH_USER_MODEL,
            dispatch_uid="create_profile_for_new_user",
        )
