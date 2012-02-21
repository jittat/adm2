from django.conf.urls.defaults import *
from models import confirmation_resource

urlpatterns = patterns(
    'confirmation.views',

    url(r'^$', 'main', name='confirmation-app-index'),
    url(r'^edit/$', 'main', 
        { 'is_edit_registration': True },
        name='confirmation-app-edit'),

    url(r'^pref/$', 'pref', name='confirmation-pref'),
    url(r'^pref-nomove/$', 'request_nomove', 
        {'is_nomove': True },
        name='confirmation-nomove-request'),
    url(r'^pref-nomove-cancel/$', 'request_nomove', 
        {'is_nomove': False },
        name='confirmation-nomove-cancel'),

    url(r'^quota/$', 'quota_confirm', name='confirmation-quota-index'),

    url(r'^quota/reset-choice/$', 
        'quota_reset_choice',
        name='confirmation-quota-reset'),

    #url(r'^registration/$', 'student_registration', name='confirmation-student-registration'),
)


urlpatterns += patterns(
    'confirmation.admin_views',

    url(r'^review/$', 'index', name='confirmation-index'),

    url(r'^review/quota/$', 'quota_stat', name='confirmation-quota-stat'),

    url(r'^review/majors/(\d+)/$', 
        'list_confirmed_applicants',
        name='confirmation-list-applicants'),

    url(r'^review/stat/$', 'confirmation_stat', name='confirmation-stat'),
    url(r'^review/stat/download/$', 'confirmation_stat_download', name='confirmation-stat-download'),
    url(r'^review/stat/download-regis/$', 'confirmation_stat_download_for_registra', name='confirmation-stat-download-regis'),
    url(r'^review/stat/download-payment-net/$', 'confirmation_payment_net_download', name='confirmation-payment-net-download'),

    url(r'^review/submit/$', 'confirm', 
        {'preview': True}, name='confirmation-submit'),
    url(r'^review/confirm/$', 'confirm', name='confirmation-confirm'),

    url(r'^review/confirm-second-round/$', 'show_confirmation_second_round', name='confirmation-second'),
    url(r'^review/confirm-second-round-admin/(\d+)/$', 'admin_show_confirmation_second_round', name='confirmation-second-admin'),

    url(r'^review/info/(\d+)/$', 'interview_info', name='confirmation-info'),
    url(r'^review/list/(.*?)/?$', confirmation_resource),
    url(r'^review/round2/$', 'confirm_round2', name='confirmation-round2'),
)
