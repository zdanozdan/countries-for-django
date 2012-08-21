from django.conf import settings
from django.conf.urls import patterns

urlpatterns = patterns('',
    (r'^setcountry/$', 'countries.views.set_country'),
)
