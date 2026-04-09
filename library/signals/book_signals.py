from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from library.models import Book



@receiver(pre_save, sender=Book)
def book_pre_save(sender, instance, **kwargs):
    print(f"Book about to be saved: {instance.title}")


@receiver(post_delete, sender=Book)
def book_deleted(sender, instance, **kwargs):
    print(f"Book deleted: {instance.title}")