
"""
This module provides functions to download videos from YouTube.
"""
from django.conf import settings
import os
import time
import urllib.request
from django.conf import settings
from urllib.error import HTTPError, URLError, ContentTooShortError
from http.client import IncompleteRead, RemoteDisconnected
from pytube import YouTube, exceptions as pytube_exceptions
from pytube.exceptions import VideoUnavailable
from rumble_uploader_app.models import YouTubeVideo

# Set up proxies
proxies = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080',
}

def download_video(youtube_link, save_path, retries=3, backoff_factor=12.5):
    """
    Download a video from YouTube.

    Args:
        youtube_link (str): The YouTube video link.
        save_path (str): The path to save the downloaded video.
        retries (int, optional): The number of retries in case of failure. Defaults to 3.
        backoff_factor (float, optional): The backoff factor for exponential backoff. Defaults to 12.5.

    Returns:
        tuple: A tuple containing the full path of the downloaded video and the thumbnail path.
    """
    retry = 0
    while retry < retries:
        try:
            yt = YouTube(youtube_link)
            video_title = yt.title

            videos_path = os.path.join(settings.MEDIA_ROOT, 'videos')

            safe_title = video_title.replace('/', '-').replace('\\', '-').replace(':', '-').replace('*', '-').replace('?', '-').replace('"', '-').replace('<', '-').replace('>', '-').replace('|', '-').replace(' ', '')
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            video_stream.download(output_path=videos_path,
                                  filename=safe_title + ".mp4")
            video_full_path = os.path.join(videos_path, safe_title + ".mp4")
            youtube_video_path_relative_path = os.path.relpath(video_full_path, settings.MEDIA_ROOT)

            thumbnail_url = yt.thumbnail_url
            thumbnail_path = os.path.join(save_path, "thumbnails", safe_title + "_thumbnail.jpg")
            urllib.request.urlretrieve(thumbnail_url, thumbnail_path)
            thumbnail_path_relative_path = os.path.relpath(thumbnail_path, settings.MEDIA_ROOT)

            #  # Save paths to YouTubeVideo model
            # youtube_video = YouTubeVideo.objects.create(
            #     youtube_video_file=youtube_video_path_relative_path,
            #     youtube_video_thumbnail=thumbnail_path_relative_path
            # )
            # youtube_video.save()

            print(f"Downloaded '{video_title}' to '{youtube_video_path_relative_path}'")
            print(f"Downloaded thumbnail to '{thumbnail_path_relative_path}'")
            return youtube_video_path_relative_path, thumbnail_path_relative_path

        except (pytube_exceptions.VideoUnavailable, HTTPError, URLError, IncompleteRead, ContentTooShortError, RemoteDisconnected) as e:
            print(f"Attempt {retry + 1} failed with error: {e}")
            if retry < retries - 1:
                sleep_time = backoff_factor * (2 ** retry)
                print(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
                retry += 1
            else:
                print(f"Failed to download video after {retries} attempts.")
                return None, None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None, None



# def download_video(youtube_link, save_path, retries=3, backoff_factor=0.3):
#     """
#     Download a video from YouTube.

#     Args:
#         youtube_link (str): The YouTube video link.
#         save_path (str): The path to save the downloaded video.
#         retries (int, optional): The number of retries in case of failure. Defaults to 3.
#         backoff_factor (float, optional): The backoff factor for exponential backoff. Defaults to 0.3.
#     """
#     for retry in range(retries):
#         try:
#             time.sleep(5)
#             yt = YouTube(youtube_link)
#             # Get the title of the video
#             video_title = yt.title

#             # Replace characters in title that are not allowed in file names
#             safe_title = video_title.replace('/', '-').replace('\\', '-').replace(':', '-').replace('*', '-').replace('?', '-').replace('"', '-').replace('<', '-').replace('>', '-').replace('|', '-')

#             # Select the highest resolution progressive stream available
#             # Select the highest resolution progressive stream available
#             video_stream = yt.streams.filter(progressive=True, file_extension='mp4') \
#                 .order_by('resolution').desc().first()
#             # Download the video with the title as the filename
#             video_stream.download(output_path=save_path, filename=safe_title + ".mp4")

#              # Construct the full path of the downloaded video
#             full_path = os.path.join(save_path, safe_title + ".mp4")

#             # Get thumbnail URL
#             thumbnail_url = yt.thumbnail_url

#             # Download thumbnail
#             thumbnail_path = os.path.join(save_path, safe_title + "_thumbnail.jpg")
#             urllib.request.urlretrieve(thumbnail_url, thumbnail_path)

#             print(f"Downloaded '{video_title}' to '{full_path}'")
#             print(f"Downloaded thumbnail to '{thumbnail_path}'")



#         except (PytubeError, VideoUnavailable, HTTPError, URLError, IncompleteRead, ContentTooShortError) as e:
#             if retry < retries - 1:  # if it's not the last attempt
#                 sleep_time = backoff_factor * (2 ** retry)  # exponential backoff
#                 print(f"Attempt {retry + 1} failed. Retrying in {sleep_time} seconds...")
#                 time.sleep(sleep_time)
#                 continue
#             print(f"Failed to download video after {retries} attempts.")
#             print(f"Error: {e}")

#     # Return the paths
#     return full_path, thumbnail_path


# def download_video(link, save_path, retries=3, backoff_factor=0.3):
#     for retry in range(retries):
#         try:
#             yt = YouTube(link)
#             mp4_streams = yt.streams.filter(file_extension='mp4').all()
#             d_video = mp4_streams[-1]
#             d_video.download(output_path=save_path)
#             print('Video downloaded successfully!')
#             return True
#         except (RemoteDisconnected, PytubeError, VideoUnavailable, VideoPrivate) as e:
#             if retry < retries - 1:  # if it's not the last attempt
#                 sleep_time = backoff_factor * (2 ** retry)  # exponential backoff
#                 time.sleep(sleep_time)
#                 continue
#             else:
#                 print(f"Failed to download video after {retries} attempts.")
#                 print(f"Error: {e}")
#                 return False


# # Set up proxies
# proxies = {
#   'http': 'http://10.10.1.10:3128',
#   'https': 'http://10.10.1.10:1080',
# }


# Working version one
# import time
# import requests
# from pytube import YouTube
# from http.client import RemoteDisconnected

# # Set up proxies
# proxies = {
#   'http': 'http://10.10.1.10:3128',
#   'https': 'http://10.10.1.10:1080',
# }

# def download_video(link, save_path, retries=3, backoff_factor=0.3):
#     for retry in range(retries):
#         try:
#             yt = YouTube(link)
#             mp4_streams = yt.streams.filter(file_extension='mp4').all()
#             d_video = mp4_streams[-1]
#             d_video.download(output_path=save_path)
#             print('Video downloaded successfully!')
#             return
#         except (RemoteDisconnected, Exception) as e:
#             if retry < retries - 1:  # if it's not the last attempt
#                 sleep_time = backoff_factor * (2 ** retry)  # exponential backoff
#                 time.sleep(sleep_time)
#                 continue
#             else:
#                 print(f"Failed to download video after {retries} attempts.")
#                 print(f"Error: {e}")
#                 return

# # Where to save
# SAVE_PATH = "D:\\Proton Drive\\My files\\rahw_coding_mobile\\aux_coding\\rumble_uploader\\rumble_upload_test_video"  # to_do

# # Links of the videos to be downloaded
# links = ["https://www.youtube.com/watch?v=MTCKan7HcEU",
#          "https://www.youtube.com/watch?v=xWOoBJUqlbI"]

# for link in links:
#     download_video(link, SAVE_PATH)
