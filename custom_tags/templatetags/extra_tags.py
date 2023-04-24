
from datetime import datetime, time

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter()
@stringfilter
def empty_space_if_none(value: str):
    value = value.lower().strip()
    if value == 'none' or value == '-':
        return ""
    return value.strip()


@register.filter()
@stringfilter
def my_date_filter(value: str):
    if value == 'None':
        return ""
    else:
        date = datetime.strptime(value, "%Y-%m-%d")
        return date.strftime('%a, %d %B, %Y')


@register.filter()
@stringfilter
def my_time_filter(value: str):
    my_time = time.fromisoformat(value)

    return str(my_time)


@register.filter()
@stringfilter
def format_text(value: str):
    if value == 'nan':
        return ""
    elif '_' in value:
        text = value.split('_')
        if len(text) <= 2:
            return " ".join(text).title()
        elif len(text) > 2:
            return "/".join(text[:2]).title() + f" {text[-1]}".title()
    else:
        return value

