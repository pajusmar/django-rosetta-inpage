import json
import logging
import simplejson
from django.http import HttpResponse
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
        print "Banaan = ", str(result), ", ", str(target_locale)

        return {
            'foo': 'bar',
            'test': 'hierzo',
        }

    @json_rsponse
    def post(self, request):
        source = request.POST.get('source', '')
        target_locale = request.POST.get('lang', '')
        target_msg = request.POST.get('msg', '')
        print "Banaan = ", str(source), ", ", str(target_locale), ", ", str(target_msg)

        return {
            'status': 'ok',
        }




'''
@csrf_exempt
@json_response
@require_POST
def create_transaction_type(request):
    """
    Create a new transaction type. You should pass `name`, `template_en`, `template_nl`, and
    `template_fr` as POST parameters.
    """
    name = request.POST.get('name', '')

    if not name:
        return HttpResponse('No name given', status=HTTP_BAD_REQUEST)

    if TransactionType.objects.filter(name=name):
        return HttpResponse('TransactionType with this name already exists', status=HTTP_CONFLICT)

    template_texts = {}

    for lang in dict(settings.LANGUAGES).keys():
        param_name = 'template_' + lang
        template_text = request.POST.get(param_name)

        if not template_text:
            return HttpResponse('Missing %s parameter' % param_name, status=HTTP_BAD_REQUEST)

        try:
            Template(template_text)
        except TemplateSyntaxError:
            return HttpResponse('%s has invalid syntax' % param_name, status=HTTP_BAD_REQUEST)

        template_texts[param_name] = template_text

    TransactionType.objects.create(name=name, **template_texts)

    return { }
'''
