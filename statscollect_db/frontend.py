from django.views.generic import TemplateView
from envelope.views import ContactView
from braces.views import FormMessagesMixin
from envelope.forms import ContactForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils.translation import ugettext_lazy as _


class HomePage(TemplateView):
    template_name = 'statnuts/homepage.html'

    # def get(self, request, *args, **kwargs):
    #     file = open(
    #         BASE_DIR +
    #         '/marketplace_rest_api/templates/marketplace/md/homepage.md',
    #         encoding='utf-8'
    #     )
    #     text = file.read()
    #     markup = markdown.markdown(text)
    #     return render(request, self.template_name, {'markup': markup})


class MyContactForm(ContactForm):
    def __init__(self, *args, **kwargs):
        super(MyContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-lg'))


class ContactPage(FormMessagesMixin, ContactView):
    form_valid_message = _(u"Thank you for your message.")
    form_invalid_message = _(u"Error : your message has not been sent.")
    form_class = MyContactForm
