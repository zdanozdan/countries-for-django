from django import http

import logging

# Create your views here.
def set_country(request):
    """
    Just remember country in session or cookie.
    Redirect to a given url while setting the chosen country in the
    session or cookie. The url and the language code need to be
    specified in the request parameters.
    """
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    response = http.HttpResponseRedirect(next)
    if request.method == 'POST':
        country_code = request.POST.get('country', None)
        if country_code:
            if hasattr(request, 'session'):
                request.session['django_country'] = country_code
            else:
                response.set_cookie(settings.COUNTRY_COOKIE_NAME, country_code)

    #return http.HttpResponse(request.POST)
    return response

