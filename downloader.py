import urllib.request
import json
import re
import unicodedata
from pytube import YouTube
import os
from dotenv import load_dotenv

load_dotenv()

# specify the id of the youtube channel
CHANNEL_ID = "UC4xKdmAXFh4ACyhpiQ_3qBw"

# need to create a dotenv file in the same directory that has a GOOGLE_API_KEY value
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

dirname = os.path.dirname(__file__)

def get_all_video_in_channel(channel_id):
    filename = os.path.join(dirname, "videos.json")
    if os.path.isfile(filename):
        print("json file exists, reading data")
        with open(filename, 'r') as input:
            data = json.load(input)
            video_links = data['video_links']
            video_titles = data['video_titles']
        return video_links, video_titles
    
    print("json file doesn't exist, creating file")

    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(GOOGLE_API_KEY, channel_id)

    video_links = []
    video_titles = []
    url = first_url
    while True:
        inp = urllib.request.urlopen(url)
        resp = json.load(inp)

        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links.append(base_video_url + i['id']['videoId'])
                video_titles.append(i['snippet']['title'])

        try:
            next_page_token = resp['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break

    with open(filename, 'w+') as outfile:
        json_dict = {
            "video_links": video_links,
            "video_titles": video_titles
        }

        json.dump(json_dict, outfile)

    return video_links, video_titles

def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

def slugify_array(array):
    # slugifies an array of strings
    new_array = []
    for item in array:
        new_item = slugify(item, True)
        new_array.append(new_item)

    return new_array

def download_videos(links, titles):
    # create downloads folder if it doesnt exist
    download_path = dirname + "/downloads"
    if not os.path.exists(download_path):
        os.mkdir(dirname + "/downloads")

    # loop through array of links and download each one
    for i in range(len(links)):
        link = links[i]
        title = titles[i]

        if os.path.isfile(os.path.join(dirname, "{}.mp4".format(title))):
            continue
        
        # some videos have errors downloading, this loop will skip those videos after 10 attempts
        count = 0
        max_error_count = 10
        while True:
            if count > max_error_count:
                print("FAILED DOWNLOAD, MOVING ON")
                break
            try: 
                print("download {}: {}".format(i, link))
                yt = YouTube(link)
                yt.streams.filter(subtype='mp4').first().download(output_path=dirname + "/downloads", filename=title)
                break
            except:
                print("error")
                count += 1
                continue
    print("complete!")

if __name__ == "__main__":
    video_links, video_titles = get_all_video_in_channel(CHANNEL_ID)

    file_safe_titles = slugify_array(video_titles)

    download_videos(video_links, file_safe_titles)