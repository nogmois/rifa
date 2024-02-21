from django import template

register = template.Library()

@register.filter(name='custom_format')
def custom_format(value, digits):
    format_string = f"0{digits}d"
    return format(value, format_string)
