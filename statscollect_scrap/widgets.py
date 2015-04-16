from django import forms
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe


class ReadOnlySelectWidget(forms.Select):
    def render(self, name, value, attrs=None, choices=()):
        if value:
            final_attrs = self.build_attrs(attrs, name=name)
            output = u'<input value="%s" type="hidden" %s>' % (value, flatatt(final_attrs))
            return mark_safe(output + str(self.choices.queryset.get(id=value)))
        else:
            return super(ReadOnlySelectWidget, self).render(name, value, attrs)
