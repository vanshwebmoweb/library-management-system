from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User



@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        print(f"New user created: {instance.username}")
        print(f"Email: {instance.email}")
        print(f"Membership date: {instance.membership_date}")


@receiver(post_save, sender=User)
def user_updated(sender, instance, created, **kwargs):
    if not created:
        print(f"User updated: {instance.username}")


@receiver(post_delete, sender=User)
def user_deleted(sender, instance, **kwargs):
    print(f"User deleted: {instance.username}")