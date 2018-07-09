from flask import Flask, request, render_template
from os import system
from subprocess import check_output

app = Flask(__name__)

@app.route('/')
def index():
  output = open('/tmp/output', 'r').read()
  return render_template('index.html', output=output)

@app.route('/refresh')
def refresh():
  exit_code = system('kill $(cat /tmp/sleep_pid)')
  status_str = 'STATUS: {}'.format(exit_code)
  return render_template('refresh.html', status=status_str)

@app.route('/set_interval')
def set_interval():
    new_interval = request.args.get('interval', None)
    if new_interval is None:
      get_running_time = \
        "ps -eo pid,etime | grep $(cat /tmp/sleep_pid) | awk '{print $2}'"
      running_time_str = \
        check_output(["bash", "-c", get_running_time]).decode().strip()
      minutes = int(running_time_str.split(':')[0])
      seconds = int(running_time_str.split(':')[1])
      running_time =  minutes * 60 + seconds

      interval = int(open('/tmp/interval', 'r').read().strip())

      return render_template(
          'set_interval.html',
          interval=interval,
          expiration=(interval - running_time))

    open('/tmp/interval', 'w').write(new_interval)
    return refresh()
