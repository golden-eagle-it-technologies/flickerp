from django.http import HttpResponseRedirect
from django.urls import reverse

from organisation_details.utils import get_organisationdetail


def organisationdetail_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        try:
            organisationdetail = get_organisationdetail(user)
            return function(request, *args, **kw)
        except:
            return HttpResponseRedirect(reverse('no_organisation_detail_page'))

    return wrapper
