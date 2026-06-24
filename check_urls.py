import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_watch.settings')
django.setup()

from django.urls import get_resolver

def show_urls(urllist, depth=0):
    for entry in urllist:
        print("  " * depth + f"→ {entry.pattern}")
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)

resolver = get_resolver()
print("\n=== Registered URLs ===")
show_urls(resolver.url_patterns)
