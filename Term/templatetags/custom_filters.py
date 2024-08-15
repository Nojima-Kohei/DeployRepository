from django import template
import markdown as md

register = template.Library()

@register.filter(name='markdown_with_breaks')
def markdown_with_breaks(value):
    return md.markdown(value, extensions=['nl2br', 'extra'])
