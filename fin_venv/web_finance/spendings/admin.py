from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from . import models

class MyUserInline(admin.StackedInline):
    model = models.MyUser
    can_delete = False
    verbose_name_plural = 'MyUser'

class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(models.categories)
admin.site.register(models.spendings)
