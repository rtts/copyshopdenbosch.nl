import re
from django import template
from markdown import markdown as md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

MARKDOWN_EXTENSIONS = ['extra', 'smarty']

phone_regex = re.compile(r'([0-9+][0-9 -]{8,}[0-9])')
email_regex = re.compile(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')

@register.simple_tag(takes_context=True)
def link(context, text):
    text = phone_regex.sub(zelda, text)
    text = email_regex.sub(zelda2, text)
    return mark_safe(md(text, extensions=MARKDOWN_EXTENSIONS))

def zelda(match):
    return '[' + match[1] + ']' + '(tel:' + match[0] + ')'

def zelda2(match):
    return '[' + match[1] + ']' + '(mailto:' + match[0] + ')'
