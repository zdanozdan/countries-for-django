"This is the locale selecting middleware that will look at accept headers"

import logging
from django.conf import settings
from django.contrib.gis.geoip import GeoIP

from locale.countries_info import COUNTRY_INFO

class CountryLocaleMiddleware(object):
    """
    This is a very simple middleware that parses a request
    and decides what country install as default if there is none selected.
    Country will be looked up using geoip library so it must be installed
    First install GeoIP C API - download and compile and install
    http://www.maxmind.com/app/c
    Then install python exception
    http://www.maxmind.com/app/python
    Need also GeoIp database
    http://www.maxmind.com/app/installation
    downoload and install in /usr/local/share/GeoIP/
    settings - path to geo ip database
    GEOIP_PATH = '/usr/local/share/GeoIP/'
    """

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def process_request(self, request):
        if hasattr(request, 'session'):
            if request.session.get('django_country') is None:
                request.session['django_country'] = settings.DEFAULT_COUNTRY
                g = GeoIP()
                ip = self.get_client_ip(request)
                if settings.DEBUG:
                    ip = '213.180.141.140' #onet.pl
                    logging.debug('DEBUG MODE: country middleware - setting country to PL based on 213.180.141.140')
                if ip is not None:
                    c = g.country_code_by_addr(ip)
                    if c in COUNTRY_INFO:
                        request.session['django_country'] = COUNTRY_INFO[c]['code']





