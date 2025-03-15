from django.apps import AppConfig


class LibraConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "libra"

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
