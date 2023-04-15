from django.contrib import admin

from session.models import Session


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass
