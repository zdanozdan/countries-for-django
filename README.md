countries-for-django
====================

This simple app will add countries list, some templatetags and post handler which will switch country and save that selection in user session.

Country list based on:
http://xml.coverpages.org/country3166.html
Country Code List: ISO 3166-1993 (E)
This international standard provides a two-letter alphabetic code for representing the names of countries, dependencies, and other areas of special geopolitical interest. The source of this code set is the "Codes for the Representation of Names of Countries (ISO 3166-1993 (E))." Note: 2005-04 correction, Nambia --> Namibia.

Install:
Check out this app as 'countries'

Configuration:
Add the countries you need to your settings.py as well as cookie name (session storage is defult)

    COUNTRY_COOKIE_NAME = 'django_country'
    COUNTRIES = (
        ('AD', gettext('Andorra')),
        ('AE', gettext('United Arab Emirates')),
        ('AF', gettext('Afghanistan')),
        ('AG', gettext('Antigua & Barbuda')),
    )

Next add urls with prefix of yours choice
    (r'^country/', include('countries.urls')),

Finally enable countries in settings.py

	INSTALLED_APPS = (
	     ...      
    	     'countries',      
	     ...
    	     # 'django.contrib.admindocs',
	)

Usage:

Create post form:

    {% load countries %}	
    {% get_current_country as country %}

    """
    this will get list of countries specified in settings.py or default list if settings are empty
    """
    {% get_available_countries as COUNTRIES %}

    <ul>
    {% get_country_info_list for COUNTRIES as countries %}
        <form action="/country/setcountry/" method="post" name="countries"> 
        {% csrf_token %}
        <!--- <input name="next" type="hidden" value="/where/to/redirect/next/" /> -->
        <select name="country">
        {% for c in countries %}
        {% ifequal c.code country %}
        <option selected="true" value="{{ c.code }}">{{ c.name }}</option>
        {% else %}
        <option value="{{ c.code }}">{{ c.name }}</option>
        {% endifequal %}
        {% endfor %}
        </select>
    <input type="submit" value="Switch Country"/>
    </form> 

Template tags: 
get_current_country

	 @register.tag("get_current_country")
	 def do_get_current_country(parser, token):
	 """
	 This will store the current country in the context.

    	 Usage::
         {% get_current_country as country %}

    	 This will fetch the currently active country and
    	 put it's value into the ``country`` context
    	 variable.
    	 """
get_country_info_list

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

get_available_countries

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

Filters:

is_eu_country filter will check if current country is in one of 27 member state
	Usage::
		{% get_current_country as country %}
		{% if country|is_eu_country %}
		EU country
		{% else %}	
		NON EU country
		{% endif %}
