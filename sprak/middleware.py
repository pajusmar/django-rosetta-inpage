# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils.html import mark_safe
from django.utils import html
from models import (THREAD_LOCAL_STORAGE, EDIT_MODE, MESSAGES)

class TranslateMiddleware(object):
    """

    """
    def __init__(self):
        pass

    def is_edit_mode(self, request):
        #return request.GET.get('translate', 'False').lower() == 'true' and request.user.is_staff
        return request.user.is_staff

    def process_request(self, request):
        """

        :param request:
        :return:
        """
        if self.is_edit_mode(request):
            setattr(THREAD_LOCAL_STORAGE, EDIT_MODE, True)
            setattr(THREAD_LOCAL_STORAGE, MESSAGES, set())
        else:
            setattr(THREAD_LOCAL_STORAGE, EDIT_MODE, False)
        return None

    def process_response(self, request, response):
        """

        :param request:
        :param response:
        :return:
        """
        if self.is_edit_mode(request):
            return self.insert_html(request, response)

        return response

    def insert_html(self, request, response):
        content = response.content
        index = content.lower().find('</body>')

        if index == -1:
            return response

        messages = getattr(THREAD_LOCAL_STORAGE, MESSAGES, set())
        html = render_to_string("sprak/sidebar.html",
            {'messages': messages_iterator(messages)},
            context_instance=RequestContext(request))

        response.content = content[:index] + html.encode("utf-8") + content[index:]
        #response.content =  unicode(s)
        return response

def messages_iterator(list):
    for msg in list:
        yield escape(encode(msg))

def encode(message):
    try:
        return message.decode().encode('utf-8')
    except UnicodeEncodeError:
        return message.encode('utf-8')

def escape(message):
    return message.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')


