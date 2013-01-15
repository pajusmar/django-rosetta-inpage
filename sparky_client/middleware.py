# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.template import RequestContext
from sparky_client import hash
from sparky_client.models import (THREAD_LOCAL_STORAGE, EDIT_MODE, MESSAGES)

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
        Only add the translation html if the status code is 200

        :param request:
        :param response:
        :return:
        """
        if self.is_edit_mode(request) and response.status_code == 200:
            return self.insert_html(request, response)

        return response

    def insert_html(self, request, response):
        content = response.content
        index = content.lower().find('</body>')

        if index == -1:
            return response

        messages = getattr(THREAD_LOCAL_STORAGE, MESSAGES, set())
        vars = {
            'messages': messages_iterator(messages),
            'count': len(messages)
        }

        html = render_to_string("sparky_client/sidebar.html", vars, context_instance=RequestContext(request))

        response.content = content[:index] + html.encode("utf-8") + content[index:]
        #response.content =  unicode(s)
        return response

def messages_iterator(list):
    for msg in list:
        yield (encode(msg), hash(msg))

def encode(message):
    try:
        return message.decode().encode('utf-8')
    except UnicodeEncodeError:
        return message.encode('utf-8')

def escape(message):
    #return message.replace('<', '&lt;').replace('>', '&gt;')
    return message.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')


