countries-for-django
====================

This simple app will add countries list, some templatetags and post handler which will switch country and save that selection in user session.

Country list based on:
http://xml.coverpages.org/country3166.html
Country Code List: ISO 3166-1993 (E)
This international standard provides a two-letter alphabetic code for representing the names of countries, dependencies, and other areas of special geopolitical interest. The source of this code set is the "Codes for the Representation of Names of Countries (ISO 3166-1993 (E))." Note: 2005-04 correction, Nambia --> Namibia.

Configuration:
Add the countries you need to your settings.py as well as cookie name (session storage is defult)

COUNTRY_COOKIE_NAME = 'django_country'
COUNTRIES = (
    ('AD', gettext('Andorra')),
    ('AE', gettext('United Arab Emirates')),
    ('AF', gettext('Afghanistan')),
    ('AG', gettext('Antigua & Barbuda')),
)

Usage:

Create post form:

{% get_current_country as country %}

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