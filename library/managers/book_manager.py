from django.db import models



class BookQuerySet(models.QuerySet):
    def available(self):
        return self.filter(copies_available__gt=0)

    def unavailable(self):
        return self.filter(copies_available=0)

    def recent(self):
        return self.order_by('-published_date',)


class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)

    def available(self):
        return self.get_queryset().available()

    def unavailable(self):
        return self.get_queryset().unavailable()

    def recent(self):
        return self.get_queryset().recent()