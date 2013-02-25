"""
Tryout some translation things
"""
from django.utils import translation
from django.utils.html import mark_safe
from django.utils.functional import lazy
from rosetta_inpage import hash
from rosetta_inpage.conf import EDIT_MODE, MESSAGES
import threading

THREAD_LOCAL_STORAGE = threading.local()

original = translation.ugettext


def _new_ugettext(message):
    mode = getattr(THREAD_LOCAL_STORAGE, EDIT_MODE, False)

    if mode:
        messages = getattr(THREAD_LOCAL_STORAGE, MESSAGES)
        messages.add(message)
        #setattr(THREAD_LOCAL_STORAGE, MESSAGES, messages)

        #print "String = " + repr(message) + ", " + str(hash(message))
        #id = hash(message)
        #return mark_safe('<span contenteditable="false" id="' + id + '">' + original(message) + '</span>')
        from django.utils.translation.trans_real import get_language
        from rosetta_inpage.utils import get_language_catalog
        lang = get_language()
        catalog = get_language_catalog(lang)
        #return original(message)
        translated = catalog.dict.get(message, None)
        if translated:
            return mark_safe(translated.msgstr)
        else:
            return original(message)
    else:
        return original(message)


def patch_ugettext():
    translation.ugettext = _new_ugettext
    translation.ugettext_lazy = lazy(_new_ugettext, unicode)


