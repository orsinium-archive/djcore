from html.parser import HTMLParser

from django.core import mail
from django.template import Context, loader
from django.test.client import Client

try:
    from django.conf import settings
    EMAIL_USERNAME = settings.EMAIL_USERNAME
    EMAIL_HOST_USER = settings.EMAIL_HOST_USER
except ImportError:
    import warnings
    warnings.warn("Can't find email settings EMAIL_USERNAME and EMAIL_HOST_USER")
    EMAIL_USERNAME, EMAIL_HOST_USER = '', ''


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    
    def handle_data(self, d):
        self.fed.append(d)
    
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class Email:
    
    def __init__(self, source_address=None, is_html=False, template='mail/base.html'):
        if source_address:
            self.source_address = source_address
        else:
            self.source_address = '{} <{}>'.format(EMAIL_USERNAME, EMAIL_HOST_USER)
        self.is_html = is_html
        self.messages = []
        self.template = loader.get_template(template)
    
    def add(self, email_address, subject, text, source_address=None):
        
        context = Context({'text': text, 'is_html': self.is_html})
        html_text = self.template.render(context)
        if self.is_html:
            text = strip_tags(text)
        
        if not source_address:
            source_address = self.source_address
        
        data = (subject, text, source_address, (email_address, ), html_text)
        self.messages.append(data)
        return data
    
    def send(self, silent=True):
        connection = mail.get_connection(fail_silently=silent)
        
        msgs = []
        for m in self.messages:
            msg = mail.EmailMultiAlternatives(*m[:4], connection=connection)
            msg.attach_alternative(m[-1], 'text/html')
            msgs.append(msg)
        
        return connection.send_messages(msgs)
