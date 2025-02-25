from django import template
from django.template.defaultfilters import stringfilter
from community.models import Community, Season, Staff
from community.const import DEFAULT_BANNERS
from typing import Union

register = template.Library()

@register.filter(name="is_staff")
def is_staff(user, staffable: Union[Community, Season]):
    if staffable.staff:
        return user.profile in staffable.staff.get_all()
    return None

@register.filter(name="capitalize")
@stringfilter
def capitalize(str):
    return str.capitalize()

@register.filter(name="get_default_banner")
def get_default_banner(format):
    if DEFAULT_BANNERS.get(format):
        return DEFAULT_BANNERS[format]
    return "images/default_banners/custom_logo.jpg"