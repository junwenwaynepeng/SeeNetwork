# user_filters.py
from django import template

register = template.Library()

@register.filter
def get_fields(value):
    return value._meta.fields

@register.filter
def get_attribute(obj, attribute_name):
    return getattr(obj, attribute_name)