import re
from faker import Faker
import random
import requests


class BaseContentAccessor():
    def get_content(self, form):
        raise NotImplementedError('get_content must be implemented by subclasses')


class CopyPasteAccessor(BaseContentAccessor):
    def get_content(self, form):
        return form.cleaned_data.get('page_content')


class URLAccessor(BaseContentAccessor):

    def __init__(self, ctrl_pattern, url_pattern):
        self.ctrl_pattern = ctrl_pattern
        self.url_pattern = url_pattern

    def get_content(self, form):
        if form.cleaned_data.get('scrapped_url'):
            url_to_scrap = form.cleaned_data.get('scrapped_url')
        else:
            url_to_scrap = self.url_pattern % form.cleaned_data.get('identifier')
        m = re.match(self.ctrl_pattern, url_to_scrap)
        if not m:
            raise ValueError('Input url %s does not match the expected url pattern of this scrapper. Scrapper\'s url '
                             'pattern is %s' % (url_to_scrap, self.ctrl_pattern))
        fake = Faker()
        headers = {
            'User-Agent': random.choice(
                [fake.chrome(), fake.firefox(), fake.safari()])
        }
        page = requests.get(url_to_scrap, headers=headers)
        return page.text