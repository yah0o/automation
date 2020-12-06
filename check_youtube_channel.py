import io
import json
import os
import ssl
import time
import urllib.request

from selenium import webdriver

# in order to avoid SSLError
ssl._create_default_https_context = ssl._create_unverified_context

PATH = "path to cloned folder"


def setup():
    # check on file existance
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        print("File videoid.json exists and readable")
    else:
        print("File is missing or is not readable, creating file...")
        with io.open(os.path.join(PATH, 'videoid.json'), 'w') as f:
            f.write(json.dumps({"videoId": ""}))
            f.close()


def check_channel():
    api_key = ""  # key to https://console.developers.google.com
    # FAQ https://developers.google.com/places/web-service/get-api-key
    channel_id = "UCMCgOm8GZkHp8zJ6l7_hIuA"  # id of a channel to check

    base_search_url = "https://www.googleapis.com/youtube/v3/search?"
    base_youtube_url = "https://www.youtube.com/watch?v="

    url = base_search_url + "key={}&channelId={}&part=snippet,id&order=date&maxResults=1".format(api_key, channel_id)
    rq = urllib.request.urlopen(url)
    resp = json.load(rq)

    videoId = resp['items'][0]['id']['videoId']

    is_video = False
    with open('videoid.json', 'r') as json_file:
        data = json.load(json_file)
        if data['videoId'] != videoId:
            print('NEW video was uploaded! Check and watch!')
            driver = webdriver.Firefox()
            driver.get(base_youtube_url + videoId)
            is_video = True
        else:
            print('NO new video on channel yet!')

    if is_video:
        with open('videoid.json', 'w') as f:
            data = {'videoId': videoId}
            json.dump(data, f)
            f.close()


try:
    while True:
        setup()
        check_channel()
        time.sleep(5)
        break
except KeyboardInterrupt:
    print('Interrupt')
