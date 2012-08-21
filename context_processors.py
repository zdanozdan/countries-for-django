from django.conf import settings # import the settings file
#from django.contrib.sessions.backends.db import SessionStore
#import datetime

def countries(context):
    return {'COUNTRIES': settings.COUNTRIES}
