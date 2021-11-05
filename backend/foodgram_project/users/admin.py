from django.contrib import admin

from .models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'follower')
    empty_value_display = "-пусто-"


admin.site.register(Subscription, SubscriptionAdmin)
