import bleach
from cryptography.fernet import Fernet
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import AuditLog

def sanitize_input(text):
    """Strip HTML tags to prevent XSS."""
    return bleach.clean(str(text), strip=True)

def encrypt_field(data):
    if not data:
        return data
    f = Fernet(settings.ENCRYPTION_KEY.encode() if isinstance(settings.ENCRYPTION_KEY, str) else settings.ENCRYPTION_KEY)
    return f.encrypt(data.encode()).decode()

def decrypt_field(encrypted_data):
    if not encrypted_data:
        return encrypted_data
    f = Fernet(settings.ENCRYPTION_KEY.encode() if isinstance(settings.ENCRYPTION_KEY, str) else settings.ENCRYPTION_KEY)
    return f.decrypt(encrypted_data.encode()).decode()

def cleanup_old_audit_logs():
    cutoff = timezone.now() - timedelta(days=settings.RETENTION_DAYS)
    AuditLog.objects.filter(timestamp__lt=cutoff).delete()

def detect_out_of_stock(stock_value):
    """Returns (is_out_of_stock, reason)"""
    import pandas as pd
    
    if pd.isna(stock_value) or stock_value == '' or stock_value is None:
        return True, 'Empty'
    
    try:
        num = float(stock_value)
        if num <= 0:
            return True, 'Zero or negative'
    except (ValueError, TypeError):
        pass
    
    s = str(stock_value).strip().lower()
    if s in ['out of stock', 'oos']:
        return True, 'Marked Out of Stock'
    
    return False, ''