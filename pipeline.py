import numpy as np
import pandas as pd
from pytube import YouTube
import time
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from moviepy.editor import VideoFileClip
from urllib.parse import urlparse, parse_qs

class Pipeline():
    def __init__(self, url):
        self.url = url
        self.full_video_name = self.get_id_from_url() + '.mp4'
        self.coords = None

        self.download_youtube_video()
        self.scrape_svg()
        Xs, ys = self.get_histogram()
        bs = self.find_clips(Xs, ys)
        self.clip_videos(bs, Xs)

    def get_id_from_url(self):
        query = parse_qs(urlparse(self.url).query)
        id = query['v']
        if not id or not len(id):
            return None
        return id[0]

    def download_youtube_video(self):
        try:
            # Create a YouTube object
            yt = YouTube(self.url)

            # Choose the stream with the highest resolution
            stream = yt.streams.get_highest_resolution()

            # Specify the download location (replace with your desired directory)
            download_dir = "/Users/mikeyjoyce/Documents/tigerhacks-2023"

            start_time = time.time()  # Record the start time

            # Download the video to the specified location
            stream.download(output_path=download_dir, filename=self.full_video_name)

            end_time = time.time()  # Record the end time
            elapsed_time = end_time - start_time

            print(f"Download complete! Time taken: {elapsed_time:.2f} seconds")
        except Exception as e:
            print("An error occurred:", str(e))

    def scrape_svg(self):
        response = requests.get(self.url)
        #DRIVER_PATH = 'chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
        driver = webdriver.Chrome()

        try:
            driver.get(self.url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
            time.sleep(10)
            button = driver.find_element_by_class_name('ytp-ad-skip-button-container')
            button.click()
            time.sleep(10)
            elements = driver.find_element(By.CLASS_NAME, 'ytp-heat-map-path')

            if elements:
                self.coords = elements.get_attribute('d')
            else:
                print("No elements with target class found on the page.")
        finally:
            driver.quit()

    def get_histogram(self):
        words = self.coords.split()

        # Initialize a list to store floating-point numbers
        nums = []

        # Iterate through the words and check if they can be converted to a float
        for word in words:
            if ',' in word:
                temp = word.split(',')
            else:
                continue

            for num in temp:
                try:
                    n = float(num)
                    nums.append(n)
                except ValueError:
                    pass

        self.coords = nums

        X, y = [], []
        isX = True
        for coord in self.coords:
            if isX:
                # Divide by 100% to make it a percentage of video elapsed
                X.append(float(coord) / 1000)
                isX = False
            else:
                y.append(float(-coord))  # (100-coord)/coord)
                isX = True

        # Normalize values
        y_arr = np.array(y)
        normalized_y = y_arr - y_arr.min()

        return X, normalized_y

    def find_clips(self, X, y):
        norm_density = y / y.sum()
        norm_density_ma = pd.Series(norm_density).rolling(10, center=True).mean().values

        peaks = find_peaks(norm_density_ma, prominence=0.0005)[0]

        plt.plot(X, norm_density_ma)

        bounds = []
        bound_magnitude = 15
        for peak in peaks:
            bounds.append((peak - bound_magnitude, peak + bound_magnitude))

        flag, last = True, bounds.copy()
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

        for i in range(len(peaks)):
            plt.axvline(X[peaks[i]], color='r')

        for i in range(len(bounds)):
            plt.axvspan(X[bounds[i][0]], X[bounds[i][1]], color='y', alpha=0.5, lw=0)
        plt.show()

        return bounds

    def clip_videos(self, bounds, X):
        video = VideoFileClip(self.full_video_path)

        count = 1
        for b in bounds:
            start = X[b[0]] * video.duration
            end = X[b[1]] * video.duration
            edited_video = video.subclip(start, end)
            file_path = str(start) + "_" + str(end) + ".mp4"
            edited_video.write_videofile(file_path, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a',
                                         remove_temp=True)
            count += 1

if __name__ == "__main__":
    p = Pipeline("https://www.youtube.com/watch?v=sqoOzGMqCQU")