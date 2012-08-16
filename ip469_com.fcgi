#!/usr/local/bin/python
#-*-mode:python; coding:utf-8-*-
#
# see Django Docs on
#   http://docs.djangoproject.com/en/dev/howto/deployment/fastcgi/
# section "Running Django on a shared-hosting provider with Apache"
# 
import sys, os

# 添加自定义Python路径
sys.path.insert(0, "/usr/local/bin/python")

# 对于大多数eggs和模块，都可以上传到用户自己目录并加以调用
#sys.path.insert(0, "/www/user.root.dir/module.upload.dir")

# 切换到工程目录（可选）
# os.chdir("/www/user.root.dir/site.mount.point/htdocs")

# 设定DJANGO_SETTINGS_MODULE环境变量
os.environ['DJANGO_SETTINGS_MODULE'] = "ip469.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")

