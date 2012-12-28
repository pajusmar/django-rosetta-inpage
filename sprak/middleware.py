# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.html import mark_safe
from django.utils import html
from models import (THREAD_LOCAL_STORAGE, EDIT_MODE, MESSAGES)

class TranslateMiddleware(object):
    """

    """
    def __init__(self):
        pass

    def is_edit_mode(self, request):
        return request.GET.get('translate', 'False').lower() == 'true'

    def process_request(self, request):
        """

        :param request:
        :return:
        """
        if self.is_edit_mode(request) and request.user.is_staff:
            setattr(THREAD_LOCAL_STORAGE, EDIT_MODE, True)
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

        html = ['<script src="' + settings.STATIC_URL + 'sprak/js/translate.js"></script>\n',
                '<link href="' + settings.STATIC_URL + 'sprak/css/translate.css" rel="stylesheet"/>\n',
                '<div class="sprak-toolbar"><ul>']

        messages = getattr(THREAD_LOCAL_STORAGE, MESSAGES, [])
        for msg in messages:
            html.append('<li>')
            html.append(encode(msg))
            html.append('</li>')

        html.append('</ul></div>')

        response.content =  content[:index] + "".join(html) + content[index:]
        return response


def encode(message):
    try:
        return escape(message.decode().encode('utf-8'))
    except UnicodeEncodeError:
        return message.encode('utf-8')

def escape(message):
    return message.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')


