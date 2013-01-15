import json
import logging
from django.http import HttpResponse

logger = logging.getLogger(__name__)


def test(request):

    dict = {'test1': 'A', 'test2': 'B'}
    str = json.dumps(dict)

    return HttpResponse(str, mimetype='application/json')

