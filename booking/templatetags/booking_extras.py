from datetime import timedelta
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def format_duration(duration):
    # If it's already a timedelta
    if hasattr(duration, "total_seconds"):
        total_minutes = duration.total_seconds() // 60

    # If it's a string like "1:30:00"
    elif isinstance(duration, str):
        try:
            h, m, s = map(int, duration.split(":"))
            total_minutes = timedelta(hours=h, minutes=m, seconds=s).total_seconds() // 60
        except Exception:
            return duration  # fallback for bad format
    else:
        return duration  # unknown format

    hours = int(total_minutes // 60)
    minutes = int(total_minutes % 60)
    return f"{hours}h {minutes}m"
