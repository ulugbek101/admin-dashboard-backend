from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(signal=post_save, sender=User)
def set_user_on_user_creation(sender, instance, created, **kwargs):
    if created:
        instance.set_password(instance.password)
        instance.username = f'{instance.first_name.capitalize()}{instance.last_name.capitalize()}'
        instance.save()
