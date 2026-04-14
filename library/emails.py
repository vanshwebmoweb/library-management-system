from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(user):
    subject = 'Welcome to Library Management System'
    message = f'''
Hi {user.name},

Welcome to our Library Management System!

Your account has been created successfully.

Username: {user.username}
Email: {user.email}
Membership Date: {user.membership_date}

You can now:
→ Browse our book collection
→ Borrow books
→ Track your borrowing history

Happy Reading!
Library Management System
    '''
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def send_borrow_confirmation_email(borrow_record):
    subject = 'Book Borrowed Successfully'
    message = f'''
Hi {borrow_record.user.name},

You have successfully borrowed a book!

Book: {borrow_record.book.title}
Author: {borrow_record.book.author.name}
Borrowed Date: {borrow_record.borrowed_date}

Please return the book on time.

Happy Reading!
Library Management System
    '''
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[borrow_record.user.email],
        fail_silently=False,
    )


def send_return_confirmation_email(borrow_record):
    subject = 'Book Returned Successfully'
    message = f'''
Hi {borrow_record.user.name},

You have successfully returned a book!

Book: {borrow_record.book.title}
Author: {borrow_record.book.author.name}
Borrowed Date: {borrow_record.borrowed_date}
Return Date: {borrow_record.return_date}

Thank you for returning the book on time!

Library Management System
    '''
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[borrow_record.user.email],
        fail_silently=False,
    )