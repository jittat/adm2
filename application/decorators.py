from django.http import HttpResponseRedirect
from commons.utils import redirect_to_index
from models import Applicant

def applicant_required(view_function):
    """
    Returns a view function that checks if the requesting user is a
    valid applicant.
    """
    def decorate(request, *args, **kwargs):
        if not 'applicant_id' in request.session:
            return redirect_to_index(request)
        try:
            applicant = (Applicant.objects.
                         select_related(depth=1).
                         get(pk=request.session['applicant_id']))
        except Applicant.DoesNotExist:
            return redirect_to_index(request)

        request.applicant = applicant
        return view_function(request, *args, **kwargs)

    return decorate

def init_applicant(view_function):
    """
    Returns a view function that checks if the requesting user is a
    valid applicant.
    """
    def decorate(request, *args, **kwargs):
        if 'applicant_id' in request.session:
            try:
                applicant = (Applicant.objects.
                             select_related(depth=1).
                             get(pk=request.session['applicant_id']))
            except Applicant.DoesNotExist:
                applicant = None
        else:
            applicant = None
        request.applicant = applicant
        return view_function(request, *args, **kwargs)

    return decorate
