from django.conf.urls.defaults import *

urlpatterns = patterns(
    'upload.views',
    url(r'^$', 'index', name='upload-index'),
    url(r'^upload/(?P<field_name>\w*)/$', 'upload', name='upload-form'),
    url(r'^progress/$', 'upload_progress', name='upload-progress'),
    url(r'^thumbnail/(\w*)\.png', 'doc_get_img', name='upload-thumbnail'),
    url(r'^preview/(\w*)\.png', 'doc_get_img', 
        { 'thumbnail': False }, name='upload-preview'),
    url(r'^submit/', 'submit', name='upload-submit'),
    url(r'^show/', 'show', name='upload-show'),
    url(r'^confirm/', 'confirm', name='upload-confirm'),

    url(r'^update/$', 'update', name='upload-update'),
)
