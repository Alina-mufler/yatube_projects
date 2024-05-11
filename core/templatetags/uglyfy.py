from django import template
register = template.Library()


@register.filter
def uglyfy(field):
    text = str()
    for i, j in enumerate(field):
        if i % 2 == 1:
            text += j.lower()
        else:
            text += j.upper()
    return text
