from django.utils import translation
from django.utils.html import mark_safe
from django.utils.functional import lazy
from rosetta_inpage.conf import EDIT_MODE, MESSAGES
import threading

THREAD_LOCAL_STORAGE = threading.local()

original = translation.ugettext


def _new_ugettext(message):
    mode = getattr(THREAD_LOCAL_STORAGE, EDIT_MODE, False)

    if mode:
        from django.utils.translation.trans_real import get_language, to_locale
        from rosetta_inpage.utils import get_message
        messages = getattr(THREAD_LOCAL_STORAGE, MESSAGES)
        messages.add(message)

        #id = hash(message)
        #return mark_safe('<span contenteditable="false" id="' + id + '">' + original(message) + '</span>')
        locale = to_locale(get_language())
        entry = get_message(message, locale)

        if entry and entry.translated():
            return mark_safe(entry.msgstr)
        else:
            return original(message)
    else:
        return original(message)


def patch_ugettext():
    translation.ugettext = _new_ugettext
    translation.ugettext_lazy = lazy(_new_ugettext, unicode)


