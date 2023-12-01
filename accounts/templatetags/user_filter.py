# user_filters.py
from django import template

register = template.Library()

@register.filter
def get_fields(value):
    return value._meta.fields

@register.filter
def get_attribute(obj, attribute_name):
    return getattr(obj, attribute_name)

@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()