from django.conf import settings
from models import THREAD_LOCAL_STORAGE, EDIT_MODE

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
            return self.insert_styling(request, response)

        return response

    def insert_styling(self, request, response):
        content = response.content
        index = content.lower().find('</body>')

        if index == -1:
            return response

        html = '<script src="' + settings.STATIC_URL + 'sprak/js/translate.js"></script>\n' \
               + '<link href="' + settings.STATIC_URL + 'sprak/css/translate.css" rel="stylesheet"/>\n ' \
               + '<div class="sprak-notify">Edit mode &raquo;</div>'

        response.content =  content[:index] + html + content[index:]
        return response


