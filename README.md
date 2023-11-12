# Rapid Reels
### First Place Prize at TigerHacks 2023

![image](https://github.com/ZackMurry/tigerhacks-2023/assets/64462489/5e6f9723-2947-4c13-87bf-1ea7cb321964)

## Overview

Rapid Reels was developed by Mikey Joyce, Zack Murry, Colin Buchheit, and Gage Smith for TigerHacks, the University of Missouri's annual hackathon,
placing first out of 33 projects in the developer category. TigerHacks 2023 took place on November 3-5 and called for projects related to the theme of "Media."

Our project is intended to address the problems creators face with the rising popularity of short-form video content on platforms like TikTok, Instagram Reels, and YouTube Shorts.
Many content creators make longer videos and then manually trim down the best parts to repost on these platforms; Rapid Reels automates this process by using data about what real
users are most entertained by, which we find by analyzing the segments users rewatch the most.


## Data Processing
To process the data we essentially broke it up into 3 essential steps:
    1. Download the data: video and replay rate heatmap
    2. Utilize a signal processing algorithm to find the maxima of the heatmap and create bounds that represent beginning and ends of clips
    3. Clip up the video at the time stamp of the given bounds and save to filesystem

Here are some graphs that help visualize the signal processing that was performed to create Rapid Reels:
![alt text](https://github.com/ZackMurry/tigerhacks-2023/images/graph1.png?raw=true)

This graph shows the replay rate histogram where at each point on the percentage axis has a replay frequency level attributed to it. The orange line is the data that was obtained from YouTube, to get the blue line we essentially found the countour of the orange line.

![alt text](https://github.com/ZackMurry/tigerhacks-2023/images/graph2.png?raw=true)

This graph shows a visualization of our signal processing algorithm. The blue line is the same contour from the previous graph, the red line is the maxima of the histogram, and lastly the yellow shaded regions are the resulting clips. We figured out that the peaks of the replay rate histogram are actually the locations of where people start watching the video again, which is why our bounds show more time that occurs after the peak. We also allowed for the bound to start before the beginning of the maxima to account for uncertainty of when the clip should begin.
