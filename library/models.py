from django.db import models
from django.conf import settings



class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='books')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='books')
    isbn = models.CharField(max_length=10,unique=True)
    published_date = models.DateField()
    copies_available = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return self.title

class BorrowRecord(models.Model):
    STATUS_CHOICES = (
        ('borrowed','Borrowed'),
        ('returned','Returned'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='borrows')
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='borrows')
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='borrowed')

    def __str__(self):
        return f"{self.user} borrowed {self.book}"

