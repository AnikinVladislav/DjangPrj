from django.contrib import admin
from .models import categories,User,spendings

# Register your models here.
class categoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "description",)

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name","surname","email","login","pswrd", "pswrd", "prediction",)

class spendingsAdmin(admin.ModelAdmin):
    list_display = ("id", "date","amount","category","user",)

admin.site.register(categories, categoriesAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(spendings, spendingsAdmin)