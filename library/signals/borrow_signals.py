from django.db.models.signals import post_save
from django.dispatch import receiver
from library.models import BorrowRecord
from library.emails import send_borrow_confirmation_email,send_return_confirmation_email



@receiver(post_save, sender=BorrowRecord)
def borrow_created(sender, instance, created, **kwargs):
    if created:
        print(f"Book borrowed!")
        print(f"User: {instance.user}")
        print(f"Book: {instance.book.title}")
        print(f"Copies remaining: {instance.book.copies_available}")

        send_borrow_confirmation_email(instance)
        print(f"Borrow confirmation email sent to {instance.user.email}")



@receiver(post_save, sender=BorrowRecord)
def borrow_updated(sender, instance, created, **kwargs):
    if not created:
        if instance.status == 'returned':
            print(f"Book returned!")
            print(f"User: {instance.user}")
            print(f"Book: {instance.book.title}")
            instance.book.copies_available += 1
            instance.book.save()
            print(f"Copies now: {instance.book.copies_available}")

            send_return_confirmation_email(instance)
            print(f"Return confirmation email sent to {instance.user.email}")