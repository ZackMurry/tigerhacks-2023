from flask import Flask, send_file, send_from_directory, request
from urllib.parse import urlparse, parse_qs

app = Flask('server')

def get_id_from_url(url):
  query = parse_qs(urlparse(url).query)
  id = query['v']
  if not id or not len(id):
    return None
  return id[0]

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


@app.route('/preview')
def preview_videos():
  url = request.args['url']
  return send_file('preview.html')

@app.route('/clips')
def get_clips():
  url = request.args['url']
  id = get_id_from_url(url)
  return ['/static/clips/0.mp4', '/static/clips/1.mp4', '/static/clips/2.mp4']
