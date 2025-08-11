
from django import template
register = template.Library()

@register.filter
def to_list(value, count):
    try:
        count = int(count)
    except:
        return []
    return list(range(1, count+1))
