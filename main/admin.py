from django.contrib import admin

from main.models import (
    User,
    RequestLog
)


admin.site.register(User)
admin.site.register(RequestLog)