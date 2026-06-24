import bleach
import pandas as pd

def sanitize_input(text):
    return bleach.clean(str(text), strip=True)

def detect_out_of_stock(stock_value):
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

def cleanup_old_audit_logs():
    from django.utils import timezone
    from datetime import timedelta
    from django.conf import settings
    from .models import AuditLog
    cutoff = timezone.now() - timedelta(days=settings.RETENTION_DAYS)
    AuditLog.objects.filter(timestamp__lt=cutoff).delete()
