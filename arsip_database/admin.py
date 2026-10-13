from django.contrib import admin

from .models import Arsip
from .models import LoginHistory

# Register your models here.
admin.site.register(Arsip)

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time')  
    list_filter = ('user', 'login_time')  