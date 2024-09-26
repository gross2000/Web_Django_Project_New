from django import template

register = template.Library()

@register.filter()
def media_filt(path):
    if path:
        return f"/media/{path}"
    return "#"