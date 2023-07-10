from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


# Create your models here.
class Test(models.Model):
    # general info
    name = models.CharField(max_length=155, verbose_name=_("Test name"))
    description = models.TextField(
        verbose_name=_("Test description"), null=True, blank=True
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="tests",
        related_query_name="user",
    )
    slug = AutoSlugField(
        populate_from="name",
        unique=True,
    )
    # timestamps
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("create timestamp")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("update timestamp"))
    deleted_at = models.DateTimeField(
        null=True, default=None, verbose_name=_("delete timestamp"), blank=True
    )

    class Meta:
        verbose_name = _("test")
        verbose_name_plural = _("tests")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
