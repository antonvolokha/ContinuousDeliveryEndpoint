import os
import sys
import subprocess

from flask import Flask, request, jsonify
app = Flask(__name__)

PORT = int(os.environ.get('BIND_PORT', 8080))
ADDRESS = os.environ.get('BIND_ADDRESS', '0.0.0.0')
SECRET = os.environ.get('SECRET', 'sfhOQKFOMBopkerokghosmbsrg')
PROJECT_DIR = os.environ.get('PROJECT_DIR', '/var/www/')
DEBUG = os.environ.get('DEBUG', True)

СOMPOSE_ACTIONS = [
  'pull',
  'down',
  'up -d',
]

def error(message):
  print(message, file=sys.stderr)
  return jsonify({'error': message})

@app.route("/pull/<name>", methods=['POST'])
def pull(name):
  global error

  name = str(name)

  if len(name) < 3:
    return '', 404

  if 'token' not in request.form:
    return error('token empty')

  token = request.form['token']

  if token != SECRET:
    return error('invalid token')

  path = "%s%s/docker-compose.yml" % (PROJECT_DIR, name)
  if not os.path.exists(path):
    dPrint("File not Found %s" % path)
    return error("File not found")

  command = ' && '.join(list(map(lambda x: "docker-compose -f %s %s" % (path, x), СOMPOSE_ACTIONS)))
  process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()

  return jsonify({
    'code': 200,
    'response': output
  })

if __name__ == '__main__':
  app.run(host=ADDRESS, port=PORT, debug=DEBUG)