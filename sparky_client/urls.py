from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'ajax/test', 'sparky_client.views.test')
)

