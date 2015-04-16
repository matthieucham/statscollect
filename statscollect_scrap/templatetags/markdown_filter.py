from django import template
from statscollect.settings import BASE_DIR
import markdown

register = template.Library()


@register.filter
def markdownify(md_file):
    file = open(
        BASE_DIR + md_file,
        encoding='utf-8'
    )
    text = file.read()
    # safe_mode governs how the function handles raw HTML
    return markdown.markdown(text)