from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


from django.contrib.auth.admin import UserAdmin
from .models import User

class UserAdmin(UserAdmin):
    model = User
    list_display = ["username", "email", "is_staff", "is_active"]

admin.site.register(User, UserAdmin)
