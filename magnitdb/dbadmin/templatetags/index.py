from django import template

register = template.Library()


@register.filter('index')
def index(list, index):
    return list[index]