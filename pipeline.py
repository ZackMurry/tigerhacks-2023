import numpy as np
import pandas as pd
from pytube import YouTube
import time
import requests
#from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from moviepy.editor import VideoFileClip
from urllib.parse import urlparse, parse_qs
from yt_dlp import YoutubeDL
import os

class Pipeline():
    def __init__(self, url):
        self.url = url
        self.full_video_name = self.get_id_from_url() + '.mp4'
        self.coords = None

        error_code = self.download_youtube_video()
        if error_code == 0:
            raise Exception('Age restricted')

        Xs, ys, vid_time = self.get_heatmap()
        bs = self.find_clips(Xs, ys, vid_time)
        self.clip_videos(bs, Xs)

    def get_id_from_url(self):
        query = parse_qs(urlparse(self.url).query)
        id = query['v']
        if not id or not len(id):
            return None
        return id[0]


    def get_heatmap(self):
        with YoutubeDL({}) as ydl:
            info = ydl.extract_info(self.url, download=False)

        start, end, val = [], [], []
        counts, i = [], 0
        for item in info['heatmap']:
            start.append(item['start_time'])
            end.append(item['end_time'])
            val.append(item['value'])
            counts.append(i / len(info['heatmap']))
            i += 1

        return counts, np.array(val), end[-1]
    def download_youtube_video(self):
        try:
            # Create a YouTube object
            yt = YouTube(self.url, use_oauth=True, allow_oauth_cache=True)

            # Choose the stream with the highest resolution
            stream = yt.streams.get_highest_resolution()

            # Specify the download location (replace with your desired directory)
            id = self.get_id_from_url()
            download_dir = f"/Users/mikeyjoyce/Documents/tigerhacks-2023/static/clips/{id}"
            os.mkdir(download_dir)

            start_time = time.time()  # Record the start time

            # Download the video to the specified location
            stream.download(output_path=download_dir, filename=self.full_video_name)

            end_time = time.time()  # Record the end time
            elapsed_time = end_time - start_time

            print(f"Download complete! Time taken: {elapsed_time:.2f} seconds")
            return 1
        except Exception as e:
            print("An error occurred:", str(e))
            return 0

    def find_clips(self, X, y, end):
        norm_density = y / y.sum()
        norm_density_ma = pd.Series(norm_density).rolling(10, center=True).mean().values

        peaks = find_peaks(norm_density_ma, prominence=0.0005)[0]

        #plt.plot(X, norm_density_ma)

        bounds = []
        s1, s2 = 15, 100
        lower_magnitude = int(50 * s1 / end)
        upper_magnitude = int(50 * s2 / end)
        for peak in peaks:
            l = max(peak - lower_magnitude, 0)
            u = min(peak + upper_magnitude, end)
            bounds.append((l, u))

        #print(bounds)

        flag, last, new_loop = True, bounds.copy(), False
        while flag:
            print(last)

            for i in range(len(last)):
                if i != len(last) - 1:
                    curr, next = last[i], last[i + 1]

                    if curr[1] >= next[0]:
                        new = (curr[0], next[1])
                        last[i] = new
                        last.remove(next)
                        new_loop = True
                        break

            if new_loop is True:
                new_loop = False
                continue

            flag = False

        if len(last) > 0:
            bounds = last

        #for i in range(len(peaks)):
        #    plt.axvline(X[peaks[i]], color='r')

        #for i in range(len(bounds)):
        #    plt.axvspan(X[bounds[i][0]], X[bounds[i][1]], color='y', alpha=0.5, lw=0)
        #plt.show()

        return bounds

    def clip_videos(self, bounds, X):
        video = VideoFileClip(self.full_video_name)

        count = 1
        download_dir = f"/Users/mikeyjoyce/Documents/tigerhacks-2023/static/clips/{id}"

        for b in bounds:
            start = X[b[0]] * video.duration
            end = X[b[1]] * video.duration
            edited_video = video.subclip(start, end)

            file_path = download_dir + str(int(start)) + "_" + str(int(end)) + ".mp4"
            edited_video.write_videofile(file_path, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a',
                                         remove_temp=True)
            count += 1

if __name__ == "__main__":
    p = Pipeline("https://www.youtube.com/watch?v=sqoOzGMqCQU")
    #p = Pipeline("https://www.youtube.com/watch?v=1b2XscG9Lfk")
    #p = Pipeline("https://www.youtube.com/watch?v=ynU-wVdesr0")