__author__ = 'Matt'
from django import template

register = template.Library()


@register.inclusion_tag('admin/statscollect_scrap/processedgame/submit_line.html', takes_context=True)
def process_submit_row(context):
    show_process = context['status'] in ('CREATED', 'PENDING', 'COMPLETE', 'AMENDED')
    show_store = context['status'] in ('PENDING', 'COMPLETE', 'AMENDED')
    ctx = {
        'show_process': show_process,
        'show_store': show_store
    }
    if context.get('original') is not None:
        ctx['original'] = context['original']
    return ctx