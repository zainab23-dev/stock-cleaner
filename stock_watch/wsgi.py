import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_watch.settings')

# ----- Cold‑start database setup -----
import django
django.setup()
from django.core.management import call_command
from apps.accounts.models import User

FLAG_FILE = '/tmp/db_initialised'

if not os.path.exists(FLAG_FILE):
    # Use a writable location for the SQLite database
    import stock_watch.settings as settings
    settings.DATABASES['default']['NAME'] = '/tmp/db.sqlite3'
    
    call_command('migrate', '--noinput')
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='Admin'
        )
    
    with open(FLAG_FILE, 'w') as f:
        f.write('done')
# ---------------------------------------

application = get_wsgi_application()
