from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def all_caps(value):
    """This template filter converts a string into all caps."""
	return value.upper()


