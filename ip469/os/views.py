# -*-coding:utf-8-*-

from django.shortcuts import render_to_response
import logging
from ip469 import settings
import subprocess
import os
import re,sys

logging.basicConfig(filename=settings.LOG_ROOT + 'os.log', level=logging.DEBUG)

enabled = True

# def execute(request, cmd, args):
#     """
#     """
#     exe=subprocess.Popen([cmd, args])

def kill_ip469(request):
    """
    """
    return kill_by_name("ip469")

# def default(request):
#     """
#     """
#     return render_to_response('ipinfo.html', locals())

def kill_by_name(name):
    cmd='ps aux|grep %(name)s | grep -v grep' % {'name':name}
    f=os.popen(cmd)
    txt=f.read()
    n_to_kill=0
    if len(txt)>=5:
        regex=re.compile(r'\w+\s+(\d+)\s+.*')
        ids=regex.findall(txt)
        n_to_kill = len(ids)
        cmd="kill -9 %(pids)s " % {'pids' : ' '.join(ids) }
        os.system(cmd)
    result_string = "killed %(n)d processes.\n%(content)s\n" % {'n':n_to_kill, 'content' : txt}
    return render_to_response('os.html', locals())

