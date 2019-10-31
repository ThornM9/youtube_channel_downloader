# youtube_channel_downloader
Python script that downloads all youtube videos in a single channel

# setup
1. Get a Google API key that has the Youtube Data API v3 enabled
2. Create a .env file in the root directory of this project and set your api key equal to GOOGLE_API_KEY
3. Specify CHANNEL_ID in downloader.py
4. Install requirements with pip (pytube, python-dotenv, etc). The requirements are visible in the first few lines of downloader.py
5. Run downloader.py

This will create a downloads folder in the same directory that has all the videos belonging to the channel id specified
