from django.contrib import admin

from apps.notifications.models import Notification

# убрать потом, как затесчу работу
admin.site.register(Notification)
