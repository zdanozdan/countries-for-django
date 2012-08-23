from django.template import (Node, Variable, TemplateSyntaxError,
    TokenParser, Library, TOKEN_TEXT, TOKEN_VAR)
from django.utils import translation

from django.contrib.sessions.backends.db import SessionStore

from ..locale.countries_info import COUNTRY_INFO

register = Library()

class GetAvailableCountriesNode(Node):
    def __init__(self, variable):
        self.variable = variable

    def render(self, context):
        from django.conf import settings
        context[self.variable] = [(k, translation.ugettext(v)) for k, v in settings.COUNTRIES]
        return ''

class GetCurrentCountryNode(Node):
    def __init__(self, variable):
        self.variable = variable

    def get_current_country(self, context):
        return context.get('request').session.get('django_country')

    def render(self, context):
        context[self.variable] = self.get_current_country(context)
        return ''

class GetCountryInfoListNode(Node):
    def __init__(self, countries, variable):
        self.countries = Variable(countries)
        self.variable = variable

    def get_country_dict(self,country_code):
        try:
            if country_code.lower() in COUNTRY_INFO:
                return COUNTRY_INFO[country_code.lower()]
            return COUNTRY_INFO[country_code]
        except KeyError:
            #pass
            raise KeyError("Unknown language code %r." % country_code)

    def get_country_info(self, country):
        # ``country`` is either a country code string or a sequence
        # with the language code as its first item
        if len(country[0]) > 1:
            return self.get_country_dict(country[0])
        else:
            return self.get_country_dict(str(country))

    def render(self, context):
        countries = self.countries.resolve(context)
        context[self.variable] = [self.get_country_info(c) for c in countries]
        return ''

@register.tag("get_current_country")
def do_get_current_country(parser, token):
    """
    This will store the current language in the context.

    Usage::

        {% get_current_country as country %}

    This will fetch the currently active language and
    put it's value into the ``language`` context
    variable.
    """
    args = token.contents.split()
    if len(args) != 3 or args[1] != 'as':
        raise TemplateSyntaxError("'get_current_country' requires 'as variable' (got %r)" % args)
    return GetCurrentCountryNode(args[2])

@register.tag("get_country_info_list")
def do_get_country_info_list(parser, token):
    """
    This will store a list of country information dictionaries for the given
    country codes in a context variable. The country codes can be specified
    either as a list of strings or a settings.COUNTRIES style tuple (or any
    sequence of sequences whose first items are country codes).

    Usage::

        {% get_country_info_list for COUNTRIES as countries %}
        {% for c in countries %}
          {{ c.code }}
          {{ c.name }}
          {{ c.name_local }}
        {% endfor %}
    """
    args = token.contents.split()
    if len(args) != 5 or args[1] != 'for' or args[3] != 'as':
        raise TemplateSyntaxError("'%s' requires 'for sequence as variable' (got %r)" % (args[0], args[1:]))

    return GetCountryInfoListNode(args[2], args[4])

@register.tag("get_available_countries")
def do_get_available_languages(parser, token):
    """
    This will store a list of available countries
    in the context.

    Usage::

        {% get_available_countries as countries %}
        {% for country in countries %}
        ...
        {% endfor %}

    This will just pull the COUNTRIES setting from
    your setting file (or the default settings) and
    put it into the named variable.
    """
    args = token.contents.split()
    if len(args) != 3 or args[1] != 'as':
        raise TemplateSyntaxError("'get_available_countries' requires 'as variable' (got %r)" % args)
    return GetAvailableCountriesNode(args[2])

