# coding: utf-8

from django import template

register = template.Library()


@register.filter(name='remove_all')
def remove_all(value, args):
    if args:
        for i in args:
            value = value.replace(i, "")
    return value