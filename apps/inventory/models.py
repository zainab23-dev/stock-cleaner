import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

class DataRow(models.Model):
    STATUS_CHOICES = [
        ('In Stock', 'In Stock'),
        ('Out of Stock', 'Out of Stock'),
    ]
    
    upload_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    row_index = models.IntegerField()
    data = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Stock')
    reason = models.CharField(max_length=120, blank=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventory_datarow'
        ordering = ['-modified_at']

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    target_type = models.CharField(max_length=50)
    target_id = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'inventory_auditlog'
        ordering = ['-timestamp']
