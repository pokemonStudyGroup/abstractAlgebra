from flask import Flask, request
from os import system

app = Flask(__name__)

@app.route('/')
def index():
  return open('/tmp/output', 'r').read()

@app.route('/refresh')
def refresh():
  return 'STATUS: {}'.format(system('kill $(cat /tmp/sleep_pid)'))

@app.route('/set_interval')
def set_interval():
    interval = request.args.get('interval', '60 * 60 * 24')
    open('/tmp/interval', 'w').write(interval)
    return refresh()
