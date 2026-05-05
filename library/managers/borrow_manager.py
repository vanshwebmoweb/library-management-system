from django.db import models


class BorrowRecordQuerySet(models.QuerySet):
    def borrowed(self):
        return self.filter(status='borrowed',)

    def returned(self):
        return self.filter(status='returned',)

    def for_user(self, user):
        return self.filter(user=user,)

    def active_borrows(self):
        return self.filter(status='borrowed',return_date__isnull=True,)


class BorrowRecordManager(models.Manager):
    def get_queryset(self):
        return BorrowRecordQuerySet(self.model, using=self._db)

    def borrowed(self):
        return self.get_queryset().borrowed()

    def returned(self):
        return self.get_queryset().returned()

    def for_user(self, user):
        return self.get_queryset().for_user(user)

    def active_borrows(self):
        return self.get_queryset().active_borrows()