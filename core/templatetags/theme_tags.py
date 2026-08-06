from django import template

from core.theme.service import ThemeService

register = template.Library()


@register.simple_tag
def current_theme():
    return ThemeService.current()
