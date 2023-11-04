from flask import Flask, send_file, send_from_directory, request

app = Flask('server')

@app.route('/')
def send_index():
  return send_file('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/video')
def process():
  url = request.args['url']
  print(url)
  return send_file('snake.html')
