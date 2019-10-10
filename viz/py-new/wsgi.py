# -*- coding: utf-8 -*-
#!/bin/python
from werkzeug.wsgi import DispatcherMiddleware
from pms3003 import pms3003

from latest_pms3003 import app as app1 
from all_pms3003 import app as app2

application = DispatcherMiddleware(pms3003, {
    '/latest_pms3003': app1.server,
    '/all_pms3003': app2.server,
})