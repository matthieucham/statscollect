from django import template
from django.conf import settings
import markdown

register = template.Library()


@register.filter
def markdownify(md_file):
    file = open(
        str(settings.APPS_DIR(md_file)),
        encoding='utf-8'
    )
    text = file.read()
    # safe_mode governs how the function handles raw HTML
    return markdown.markdown(text)