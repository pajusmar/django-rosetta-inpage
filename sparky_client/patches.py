"""
Tryout some translation things
"""
from django.utils import translation
from django.utils.functional import lazy
from sparky_client.models import (THREAD_LOCAL_STORAGE, EDIT_MODE, MESSAGES)

original = translation.ugettext

def _new_ugettext(message):
    mode = getattr(THREAD_LOCAL_STORAGE, EDIT_MODE, False)

    if mode:
        messages = getattr(THREAD_LOCAL_STORAGE, MESSAGES)
        messages.add(message)
        setattr(THREAD_LOCAL_STORAGE, MESSAGES, messages)

        #return mark_safe(u'<span contenteditable="true" class="sprak-msg" data="">' + original(message) + '</span>')
        #return mark_safe(u"<span contenteditable='true' class='sprak-msg' data=''>" + original(message) + "</span>")
        return original(message)
    else:
        return original(message)

def patch_ugettext():
    translation.ugettext = _new_ugettext
    translation.ugettext_lazy = lazy(_new_ugettext, unicode)




"""
def patch():
    print "The great patch of ugettext"

    original = translation.ugettext
    def _ugettext_patch(message):
        print "Patch uget"
        return "<span contenteditable='true'>" + original(message) + "</span>"
    translation.ugettext = _ugettext_patch


    #def do_translate(parser, token):
    orig = trans_real.do_translate
    def _do_translate(parser, token):
        print "Trans trans " + str(token)
        return "<span contenteditable='true'>" + orig(parser, token) + "</span>"
    trans_real.do_translate = _do_translate


"""

