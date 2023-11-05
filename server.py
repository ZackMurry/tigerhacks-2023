from flask import Flask, send_file, send_from_directory, request
from urllib.parse import urlparse, parse_qs
from pipeline import Pipeline
import threading
import os

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

def start_pipeline(url):
  Pipeline(url)

@app.route('/video')
def process():
  url = request.args['url']
  print(url)
  threading.Thread(target=start_pipeline, args=(url,)).start()
  return send_file('snake.html')


@app.route('/preview')
def preview_videos():
  url = request.args['url']
  return send_file('preview.html')

@app.route('/clips')
def get_clips():
  url = request.args['url']
  id = get_id_from_url(url)
  dir = f"/Users/mikeyjoyce/Documents/tigerhacks-2023/static/clips/{id}/"
  if not os.path.exists(dir):
    return '0'
  files = os.listdir(dir)
  vid_name = dir + id + ".mp4"
  if vid_name in files: files.remove(vid_name)
  print(files)
  return ['/static/clips/0.mp4', '/static/clips/1.mp4', '/static/clips/2.mp4']



@app.route('/status')
def get_status():
  url = request.args['url']
  id = get_id_from_url(url)
  num = request.args['num']

  dir = f"/Users/mikeyjoyce/Documents/tigerhacks-2023/static/clips/{id}/"
  if not os.path.exists(dir):
    return '0'
  files = os.listdir(dir)
  print(files)
  return '1' if len(files) > 1 else '0'
