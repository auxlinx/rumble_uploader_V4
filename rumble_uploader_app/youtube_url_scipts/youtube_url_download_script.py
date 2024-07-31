
"""
This module provides functions to download videos from YouTube.
"""
import subprocess
from django.conf import settings
import os
import time
import urllib.request
from django.conf import settings
from urllib.error import HTTPError, URLError, ContentTooShortError
from http.client import IncompleteRead, RemoteDisconnected, IncompleteRead
from pytube import YouTube, exceptions as pytube_exceptions
from requests.exceptions import ConnectionError, ChunkedEncodingError, HTTPError
from urllib.error import HTTPError


# Set up proxies
proxies = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080',
}


# # Define the base path to the protonvpn_cli directory
# protonvpn_base_path = r"env\Lib\site-packages\protonvpn_cli"

# # Construct the full path to the protonvpn executable
# # Assuming the executable is named 'protonvpn-cli' and is located in the specified directory
# protonvpn_executable_path = os.path.join(protonvpn_base_path, "protonvpn-cli")

# def change_vpn():
#     # Disconnect from the current VPN server
#     subprocess.run([protonvpn_executable_path, "d"], check=True)
#     time.sleep(5)  # Wait a bit for the disconnection to complete

#     # Reconnect to a random VPN server
#     subprocess.run([protonvpn_executable_path, "c", "-r"], check=True)
#     time.sleep(10)  # Wait a bit for the connection to establish


def download_youtube_video(youtube_link, save_path, retries=3, backoff_factor=1):
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
            # change_vpn()
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

            print(f"Downloaded '{video_title}' to '{youtube_video_path_relative_path}'")
            print(f"Downloaded thumbnail to '{thumbnail_path_relative_path}'")
            return youtube_video_path_relative_path, thumbnail_path_relative_path

        except HTTPError as e:
            if e.code == 429:  # Rate limited
                retry_after = e.headers.get("Retry-After")
                wait = int(retry_after) if retry_after else backoff_factor * (2 ** retry)
                print(f"Rate limited. Retrying in {wait} seconds...")
                time.sleep(wait)
                retry += 1
            else:
                print(f"HTTP error occurred: {e}")
                return None, None
        except IncompleteRead:
            # Oh well, reconnect and keep trucking
            continue  #
        except (pytube_exceptions.VideoUnavailable, HTTPError, URLError, ContentTooShortError, RemoteDisconnected, ConnectionError, ChunkedEncodingError) as e:
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
