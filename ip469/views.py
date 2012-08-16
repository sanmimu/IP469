# -*-coding:utf-8-*-

from django.shortcuts import render_to_response
from django.shortcuts import redirect
import logging
from ip469 import settings

logging.basicConfig(filename=settings.LOG_ROOT + 'default.log',
                    level=logging.DEBUG)

def default(request):
    """
    """
    return redirect('/tuan/')
