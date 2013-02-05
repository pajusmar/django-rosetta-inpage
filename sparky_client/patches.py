"""
Tryout some translation things
"""
from django.utils import translation
from django.utils.html import mark_safe
from django.utils.functional import lazy
from sparky_client import hash
from sparky_client.models import (THREAD_LOCAL_STORAGE, EDIT_MODE, MESSAGES)

original = translation.ugettext

def _new_ugettext(message):
    mode = getattr(THREAD_LOCAL_STORAGE, EDIT_MODE, False)

    if mode:
        messages = getattr(THREAD_LOCAL_STORAGE, MESSAGES)
        messages.add(message)
        setattr(THREAD_LOCAL_STORAGE, MESSAGES, messages)

        #print "String = " + repr(message) + ", " + str(hash(message))
        id = hash(message)
        #return mark_safe('<span contenteditable="false" id="' + id + '">' + original(message) + '</span>')
        return original(message)
    else:
        return original(message)


def patch_ugettext():
    translation.ugettext = _new_ugettext
    translation.ugettext_lazy = lazy(_new_ugettext, unicode)


