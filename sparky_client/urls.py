from django.conf.urls.defaults import patterns, url
from sparky_client.views import MessageView

urlpatterns = patterns('',
    #url(r'ajax/message', 'sparky_client.views.save_message' ),
    url(r'ajax/message', MessageView.as_view()),
)

