from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.tests.models import AssignedTest

from .models import Notification


@receiver(post_save, sender=AssignedTest)
def create_notification_on_assign(sender, instance, created, **kwargs):
    """создаем уведомление при назначении теста"""
    if created:
        instance.notifications.create(
            user=instance.assigned_to,
            subject=Notification.NotificationTypes.TEST_ASSIGNED,
            text=f"Пользователь {instance.assigned_by} назначил вам тест {instance.test.title}",
        )
