import logging
import simplejson

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.translation import trans_real

logger = logging.getLogger(__name__)


def json_rsponse(view):
    '''
    Decorator view to generate a json response

    @param view:
    @return:
    '''
    def _json_response(*args, **kwargs):
        result = view(*args, **kwargs)

        if isinstance(result, HttpResponse):
            return result
        else:
            return HttpResponse(simplejson.dumps(result), content_type='application/json; charset=utf-8')
    return _json_response


class MessageView(View):
    @json_rsponse
    def get(self, request):
        source = request.GET.get('source', '')
        target_locale = request.GET.get('lang', '')
        result = trans_real.ugettext(source)

        return {
            'foo': 'bar',
            'test': '42',
        }

    @csrf_exempt
    @json_rsponse
    def post(self, request):
        source = request.POST.get('source', '')
        target_locale = request.POST.get('lang', '')
        target_msg = request.POST.get('msg', '')
        #print "Post 1 = ", str(source), ", ", str(target_locale), ", ", str(target_msg)
        #print "Post 1.1 = ", str(settings.SOURCE_LANGUAGE_CODE), ", ", str(request.LANGUAGE_CODE)

        import os
        from django.utils.translation.trans_real import get_language
        from rosetta import storage
        from rosetta.poutil import find_pos
        from rosetta.polib import pofile
        from rosetta_inpage.utils import get_language_catalog

        # file_ = find_pos(langid, project_apps=project_apps, django_apps=django_apps,
        # third_party_apps=third_party_apps)[int(idx)]
        stor = storage.get_storage(request)
        pos = find_pos('nl-nl', third_party_apps=True)
        print "Post = ", repr(stor), ", ", repr(pos)

        lang = get_language()
        catalog = get_language_catalog(lang)
        translated = catalog.dict.get(source, None)

        if translated:
            translated.msgstr = target_msg

        for p in pos:
            file = pofile(p)
            msg = file.find(source)

            if msg:
                msg.msgstr = target_msg
                msg.obsolete = False
                file.save()
                #po_filepath, ext = os.path.splitext(p)
                #save_as_mo_filepath = po_filepath + '.mo'
                #file.save_as_mofile(save_as_mo_filepath)
                print "Msg = ", repr(msg), ", ", str(p)

        return {
            'status': 'ok',
        }
