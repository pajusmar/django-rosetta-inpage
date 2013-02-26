# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils.html import mark_safe

from rosetta_inpage import hash
from rosetta_inpage.conf import EDIT_MODE, MESSAGES
from rosetta_inpage.patches import THREAD_LOCAL_STORAGE
from rosetta_inpage.utils import encode, get_locale_catalog


class TranslateMiddleware(object):
    """
    Adds an extra html toolbar (and css & js) to translate strings if the user is a staff user.
    After the response content is rendered this middleware will insert the html
    """
    def is_edit_mode(self, request):
        #return request.GET.get('translate', 'False').lower() == 'true' and request.user.is_staff
        return request.user.is_staff and getattr(settings, 'ROSETTA_INPAGE', False)

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
        if self.is_edit_mode(request) and response.status_code == 200 and not request.path.startswith('/rosetta'):
            return self.insert_html(request, response)

        return response

    def insert_html(self, request, response):
        content = response.content
        index = content.lower().find('</body>')

        if index == -1:
            return response

        messages = getattr(THREAD_LOCAL_STORAGE, MESSAGES, set())
        viewer = messages_viewer(messages)
        percentage = 100 * float(viewer[1]) / float(len(messages))
        dictionary = {
            'rosetta_inpage': {
                'messages': viewer[0],
                'translate_from': str(settings.SOURCE_LANGUAGE_CODE.split('-')[0]),
                'translate_to': str(request.LANGUAGE_CODE),
                'stats': {
                    'count': len(messages),
                    'translated': viewer[1],
                    'percentage': percentage,
                }
            }
        }

        html = render_to_string("rosetta_inpage/sidebar.html", dictionary, context_instance=RequestContext(request))
        response.content = content[:index] + html.encode("utf-8") + content[index:]
        #response.content =  unicode(s)
        return response


def messages_viewer(list_messages):
    """
    Use the original translate function instead of the patched one
    """
    from django.utils.translation.trans_real import get_language, to_locale
    from rosetta_inpage.patches import original as _  # The original

    results = []
    locale = to_locale(get_language())
    catalog = get_locale_catalog(locale)
    translated_count = 0

    def create(msg):
        translated = catalog.dict.get(msg, None)
        is_valid_translation = True if translated and translated.msgstr is not u"" or None \
            and not translated.obsolete else False

        # if translated:
        #    print "\n\n", str(is_valid_translation), ", "
        #    print "Test= ", msg, translated, "==", encode(translated.msgstr), \
        #        ", file=", str(translated.pfile), "obs=", str(translated.obsolete), "\n"

        if is_valid_translation:
            msg_target = translated.msgstr
        else:
            msg_target = _(msg)

        return {
            'show': encode(msg),
            'hash': hash(msg),
            'source': mark_safe(msg),       # the source message
            'msg': mark_safe(msg_target),   # the translated message
            'translated': is_valid_translation,
        }

    for msg in list_messages:
        item = create(msg)
        results.append(item)
        if item.get('translated', False):
            translated_count += 1

    return results, translated_count
