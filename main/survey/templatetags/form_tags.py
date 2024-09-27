from django import template

register = template.Library()

@register.simple_tag
def form_errors(field):
    if field.errors:
        return f'<span class="text-red-500 text-bold text-sm">{", ".join(field.errors)}</span>'
    return ''
