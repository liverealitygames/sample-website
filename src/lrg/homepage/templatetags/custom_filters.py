from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def to_string(value):
    return str(value)

@register.filter(name="to_html")
@stringfilter
def to_html(text: str):
    return text.replace("\n", "<br>")