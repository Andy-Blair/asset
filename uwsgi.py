"""
WSGI config for yytx project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import sys  
import os  
  
sys.path.append(os.path.abspath(os.path.dirname(__file__)))  
sys.path.append('/var/www')  
os.environ['DJANGO_SETTINGS_MODULE'] = 'yytx.settings'  
  
import django.core.handlers.wsgi  
  
application = django.core.handlers.wsgi.WSGIHandler() 
