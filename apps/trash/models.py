from django.db import models
from django.conf import settings
from django.utils import timezone

class Trash(models.Model):
    original_row_id = models.IntegerField()
    data = models.JSONField()
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    deleted_at = models.DateTimeField(default=timezone.now)
    restored = models.BooleanField(default=False)

    class Meta:
        db_table = 'trash_trash'
        ordering = ['-deleted_at']
        verbose_name_plural = 'Trash'
