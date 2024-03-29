from django.conf.urls.defaults import *

urlpatterns = patterns(
    'review.views',

    url(r'^$', 'index', name='review-index'),

    url(r'^list/all/$', 'list_applicant', name='review-list-all'),
    url(r'^list/paid/$', 'list_applicant',
        { 'paid': True }, name='review-list-paid'),
    url(r'^list/score-imported/$', 'list_applicant',
        { 'score_imported': True }, name='review-list-score-imported'),
    url(r'^list/broken-score-imported/$', 'list_applicant',
        { 'score_imported': False }, name='review-list-broken-score-imported'),
    url(r'^list/complete/$', 'list_applicant',
        { 'paid': True, 'score_imported': True }, name='review-list-complete'),

    url(r'^ticket/$', 'verify_ticket', name='review-ticket'),
    url(r'^show_app/(\d+)/$', 'show_applicant', 
        name='review-show-app'),

    url(r'^show_app/(\d+)/payment/new', 'create_payment', 
        name='review-app-create-payment'),

    url(r'^export/app-nat-id/$', 'export_app_nat_id',
        name='review-export-app-nat-id'),
    url(r'^import/scores/$', 'import_niets_scores',
        name='review-import-niets-scores'),
    url(r'^import/scores/real/$', 'import_niets_scores', 
        { 'testing':False },
        name='review-import-niets-scores-real'),

    url(r'^search/$', 'search', name='review-search'),

    url(r'^stat/major_pref/$', 'show_major_pref_stat',
        name='review-stat-major-pref'),

    url(r'^show/(\d+)/$', 'review_document', name='review-show'),
    url(r'^show/(\d+)/manual/$', 'review_document', 
        { 'return_to_manual': True }, name='review-show-after-manual'),
    url(r'^received/toggle/(\d+)/$', 'toggle_received_status', 
        name='review-toggle-received-status'),

    url(r'^gen-password/(\d+)/$', 'generate_password', 
        name='review-gen-password'),

    url(r'^reviewall/$', 'auto_review_all_apps',
        name='review-auto-review-all'),

    url(r'^list/qualified/$', 'list_qualified_applicants',
        { 'download': True }, name='review-download-list-qualified'),



    url(r'^list/incomplete/postal$', 'list_incomplete_applicants',
        { 'submission_method': 'postal' },
        name='review-list-incomplete-postal'),
    url(r'^list/incomplete/offline$', 'list_incomplete_applicants',
        { 'submission_method': 'offline' },
        name='review-list-incomplete-offline'),
    url(r'^list/incomplete/online$', 'list_incomplete_applicants',
        { 'submission_method': 'online' },
        name='review-list-incomplete-online'),

    url(r'^list/supplements/$', 'list_applicants_with_supplements',
        name='review-list-supplements'),

    url(r'^list/inspect/supplements/$', 'list_applicants_with_supplements',
        { 'time_diff': '00:10:00', 'review_status': None },
        name='review-list-inspect-supplement'),
    url(r'^list/inspect/update/$', 
        'list_applicants_with_potential_edu_update_hazard',
        name='review-list-inspect-edu-update'),

    url(r'^view/(\d+)/(\w+)/', 'doc_view', name='review-doc-view'),
    url(r'^supplement/view/(\w+)/', 
        'supplement_view', name='review-supplement-view'),
    url(r'^img/(\d+)/(\w*)', 'doc_img_view', name='review-doc-img-view'),
    url(r'^supplement/img/(\w*)', 'supplement_img_view', 
        name='review-supplement-img-view'),

)
