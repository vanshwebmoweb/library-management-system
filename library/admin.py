from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Author,Category,Book,BorrowRecord

User = get_user_model()  

class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'borrowed_date', 'return_date', 'status']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
     

    
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(BorrowRecord,BorrowRecordAdmin)
