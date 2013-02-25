from django.conf.urls.defaults import patterns, url
from rosetta_inpage.views import MessageView, GitHubView

urlpatterns = patterns('',
                       #url(r'ajax/message', 'rosetta_inpage.views.save_message' ),
                       url(r'ajax/message', MessageView.as_view(), name='rosetta-inpage-message'),
                       url(r'ajax/github', GitHubView.as_view(), name='rosetta-inpage-github'),
                       )

