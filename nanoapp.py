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
ip_addr = gethostbyname(gethostname())

@app.route('/')
def index():
    return(f'{header}<pre>nanoapp: Hello, world!\n\n{ip_addr}; {datetime.now()}</pre>{footer}')

@app.route('/env')
def print_env():
    html = header + f'<pre>_IP_ADDR = {ip_addr}\n_NOW = {datetime.now()}\n\n'
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

