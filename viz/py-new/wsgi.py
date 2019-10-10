# -*- coding: utf-8 -*-
#!/bin/python
from werkzeug.wsgi import DispatcherMiddleware
from pms3003 import pms3003

from latest import app as app1 
from all import app as app2

application = DispatcherMiddleware(pms3003, {
    '/latest': app1.server,
    '/all': app2.server,
})