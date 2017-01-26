__author__ = 'zhangyan'

import sys
sys.path.insert(0, './django_pro')
from django_pro import wsgi


app = wsgi.application

