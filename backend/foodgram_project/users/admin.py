from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Subscription

User = get_user_model()


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'follower')
    empty_value_display = "-пусто-"


class ReUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    empty_value_display = "-пусто-"


admin.site.unregister(User)
admin.site.register(User, ReUserAdmin)

admin.site.register(Subscription, SubscriptionAdmin)
