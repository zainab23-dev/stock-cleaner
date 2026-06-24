from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.conf import settings
from .models import DataRow
from apps.accounts.models import Preference

scheduler = BackgroundScheduler()

def check_stock_and_notify():
    """Check for out of stock items and notify users."""
    try:
        out_of_stock_count = DataRow.objects.filter(status='Out of Stock').count()
        
        if out_of_stock_count > 0:
            users_to_notify = Preference.objects.filter(
                email_notifications=True
            ).select_related('user')
            
            for pref in users_to_notify:
                send_mail(
                    subject=f'Stock Alert: {out_of_stock_count} items out of stock',
                    message=f'There are currently {out_of_stock_count} items out of stock in the inventory system.\n\nPlease check the dashboard for more details.',
                    from_email=settings.EMAIL_HOST_USER or 'noreply@stockwatch.com',
                    recipient_list=[pref.user.email],
                    fail_silently=True,
                )
    except Exception as e:
        print(f"Scheduler error: {e}")

def start_scheduler():
    """Initialize and start the background scheduler."""
    try:
        # Only add job if not already added
        if not scheduler.get_jobs():
            scheduler.add_job(
                check_stock_and_notify,
                'interval',
                minutes=15,
                id='stock_check',
                replace_existing=True
            )
            scheduler.start()
            print("Scheduler started successfully")
    except Exception as e:
        print(f"Failed to start scheduler: {e}")