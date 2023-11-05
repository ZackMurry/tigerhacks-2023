from yt_dlp import YoutubeDL

url = 'https://www.youtube.com/watch?v=z_e7weCwimc'
with YoutubeDL({}) as ydl:
  # res = ydl.download([url])
  info = ydl.extract_info(url)
  print(info.keys())
  print(info['heatmap'])