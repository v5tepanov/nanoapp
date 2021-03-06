from flask import Flask
from markupsafe import escape
from os import environ
from socket import gethostbyname, gethostname
from datetime import datetime


header = ('<!DOCTYPE html><header><style type="text/css">'
          'pre {font-family: Consolas; font-size: 12px;}</style>'
          '<title>nanoapp</title></header><body>')
footer = '</body></html>'

app = Flask(__name__)

@app.route('/')
def index():
    html =  f'nanoapp: Hello, world!\n\n{datetime.now()}\n\n'
    html += '<a href="/env">/env</a>'
    return(f'{header}<pre>{html}</pre>{footer}')

@app.route('/env')
def print_env():
    ip_addr = gethostbyname(gethostname())
    html = header + f'<pre>IP_ADDR = {ip_addr}\nNOW = {datetime.now()}\n\n'
    for var in environ:
        html += f'{var} = {escape(environ[var])}\n'
    html += '</pre>' + footer
    return(html)

@app.route('/print/<s>')
def print_str(s):
    return(f'{header}<pre>{escape(s)}</pre>{footer}')

@app.route('/healthy')
def liveness_probe():
    return(f'{header}<pre>Yes</pre>{footer}')

@app.route('/ip')
def ip():
    ip_addr = gethostbyname(gethostname())
    return(f'{header}<pre>{ip_addr}</pre>{footer}')

@app.route('/help')
def help():
    html =  '<a href="/">/</a>\n'
    html += '<a href="/env">/env</a>\n'
    html += '<a href="/healthy">/healthy</a>\n'
    html += '<a href="/ip">/ip</a>\n'
    html += '<a href="/print/STRING">/print/STRING</a>'
    return(f'{header}<pre>{html}</pre>{footer}')

@app.errorhandler(404)
def not_found(err):
    return(f'{header}<pre>{err}</pre>{footer}'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

