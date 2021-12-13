from flask import Flask
from markupsafe import escape
from os import environ, getpid, kill
from sys import getsizeof
from random import randint
from signal import SIGTERM
from socket import gethostbyname, gethostname
from datetime import datetime

from werkzeug.utils import redirect


header = ('<!DOCTYPE html><header><style type="text/css">'
          'pre {font-family: Consolas; font-size: 12px; line-height: 1em; margin: 1em 1em 1em 1em;}</style>'
          '<title>nanoapp</title></header><body>')
footer = '</body></html>'
buf = []
cpustress = False

app = Flask(__name__)

@app.route('/')
def index():
    global cpustress
    global buf
    with open('/proc/self/status') as f:
        memusage = f.read().split('VmRSS:')[1].split('\n')[0][:-3]
    host = gethostname()
    ip = gethostbyname(host)
    now = str(datetime.now())
    html =   '<span style="color:lightgrey">┌───────────────────┐<br>'
    html +=  '│ <span style="color:green"> *** nanoapp *** </span> │<br>'
    html += f'└───────────────────┘</span><br>'
    html +=  '<span style="line-height:1.2em"><br>'

    html += f' hostname: {host}<br>'
    html += f' IP addr : {ip}<br>'
    # html += f' timestamp : {now}<br>'
    # html +=  '<br> <a href="/dbtest"    style="color:blue">DBTEST</a>    - check access to PostgreSQL or Redis database'

    # if cpustress:
    #     html += '<br> CPUSTRESS - <span style="color:red">IN PROGRESS</span>'
    # else:
    #     html += '<br> <a href="/cpustress" style="color:blue" onclick="return confirm(\'Do you really want to STRESS CPU at a server side? Click OK to continue.\');">CPUSTRESS</a> - stress CPU for 10 minutes'

    # html += f'<br> <a href="/eatmemory" style="color:blue" onclick="return confirm(\'Do you really want to eat +230KB of memory? Click OK to continue.\');">EATMEMORY</a> - eat +230KB of memory (currently use {int(memusage.strip()):,}kB)'
    # html +=  ('<br> <a href="/kill"      style="color:blue" '
    #           'onclick="return confirm(\'Do you really want to KILL this app at server side? '
    #           'Click OK to continue.\');">KILL</a>    - terminate (simulate POD crash)<br>'
    #           '</span>')

    html += '<br><span style="color:grey">'
    for var in sorted(environ):
        html += f' {var} = {escape(environ[var])}  \n'

    return(f'{header}<pre>{html}</span></span></pre>{footer}')

@app.route('/kill')
def crash():
    kill(getpid(), SIGTERM)

@app.route('/cpustress')
def cpu_stress():
    global cpustress
    cpustress = True
    return redirect('/')

@app.route('/eatmemory')
def eat_memory():
    global buf
    current_size = getsizeof(buf)
    target_size = current_size + (1024*1024*31) # ~230KB
    while getsizeof(buf) < target_size:
        buf.append(randint(1,9999999999999999999999999))
    return redirect('/')

@app.errorhandler(404)
def not_found(err):
    return(f'{header}<pre> {err}</pre>{footer}'), 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
