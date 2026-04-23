from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from library.emails import send_welcome_email



User = get_user_model()


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        print(f"New user registered: {instance.username}")

        send_welcome_email(instance)
        print(f"Welcome email sent to {instance.email}")