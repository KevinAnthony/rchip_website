from django import template

register = template.Library()
@register.filter(name='currency')
def currency(decimal):
    dollars = float(dollars)
    return "$%s%s" % (int(dollars), ("%0.2f" % dollars)[-3:])

