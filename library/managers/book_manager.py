from django.db import models



class BookQuerySet(models.QuerySet):

    def available(self):
        return self.filter(copies_available__gt=0)

    def unavailable(self):
        return self.filter(copies_available=0)

    def by_author(self, author_id):
        return self.filter(author__id=author_id)

    def by_category(self, category_id):
        return self.filter(category__id=category_id)

    def recent(self):
        return self.order_by('-published_date',)


class BookManager(models.Manager):

    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)

    def available(self):
        return self.get_queryset().available()

    def unavailable(self):
        return self.get_queryset().unavailable()

    def by_author(self, author_id):
        return self.get_queryset().by_author(author_id)

    def by_category(self, category_id):
        return self.get_queryset().by_category(category_id)

    def recent(self):
        return self.get_queryset().recent()