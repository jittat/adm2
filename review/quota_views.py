from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from application.models import Applicant, Major
from application.models import SubmissionInfo

@login_required
def list_by_majors(request):
    applicants = []
    submission_infos = SubmissionInfo.objects.order_by('-submitted_at').select_related(depth=1)

    majors = Major.get_all_majors()

    major_lists = dict([(int(m.number),{'major': m, 'applicants': []})
                        for m in majors])

    for s in submission_infos:
        applicant = s.applicant
        major_num = applicant.preference.majors[0]
        major_lists[major_num]['applicants'].append(applicant)

    return render_to_response("review/list_applicants_by_majors.html",
                              { 'major_lists': major_lists })
