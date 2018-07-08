from flask import Flask, request
from os import system
from subprocess import check_output

app = Flask(__name__)

INDEX_TEMPLATE = """
<html>
<a href=http://18.220.120.4/refresh>Backup now</a><br>
<a href=http://18.220.120.4/set_interval>Set interval</a><br>
{}
</html>
"""
@app.route('/')
def index():
  output = open('/tmp/output', 'r').read().replace('\n', '<br>')
  return INDEX_TEMPLATE.format(output)

REFRESH_TEMPLATE = """
<html>
{}<br>
<a href=http://18.220.120.4/>index</a>
</html>
"""
@app.route('/refresh')
def refresh():
  status = 'STATUS: {}'.format(system('kill $(cat /tmp/sleep_pid)'))
  return REFRESH_TEMPLATE.format(status)

INTERVAL_TEMPLATE = """
<html>
Interval is currently {}.<br>
{}s until current interval expires.<br>
To set interval use /set_interval?interval=(interval in s).<br>
<a href=http://18.220.120.4/>index</a>
</html>
"""
@app.route('/set_interval')
def set_interval():
    interval = request.args.get('interval', None) 
    if interval is None:
      get_running_time = \
        "ps -eo pid,etime | grep $(cat /tmp/sleep_pid) | awk '{print $2}'"
      running_time_str = \
        check_output(["bash", "-c", get_running_time]).decode().strip()
      minutes = int(running_time_str.split(':')[0])
      seconds = int(running_time_str.split(':')[1])
      running_time =  minutes * 60 + seconds 

      interval = int(open('/tmp/interval', 'r').read().strip())

      return INTERVAL_TEMPLATE.format(interval, interval - running_time)
    open('/tmp/interval', 'w').write(interval)
    return refresh()
