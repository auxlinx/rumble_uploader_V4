
"""
This module provides functions to download videos from YouTube.
"""
import os
import time
import urllib.request
import logging

from urllib.error import URLError, ContentTooShortError, HTTPError
from http.client import IncompleteRead, RemoteDisconnected
from django.conf import settings
from pytube import YouTube, exceptions as pytube_exceptions
from requests.exceptions import ChunkedEncodingError
from urllib.error import HTTPError as urllib_HTTPError

logger = logging.getLogger(__name__)


# Set up proxies
proxies = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080',
}

def download_youtube_video(youtube_video_url, save_path, retries=3, backoff_factor=1):
    """
    Download a video from YouTube.

    Args:
        youtube_video_url (str): The YouTube video link.
        save_path (str): The path to save the downloaded video.
        retries (int, optional): The number of retries in case of failure. Defaults to 3.
        backoff_factor (float, optional): The backoff factor for exponential backoff. Defaults to 12.5.

    Returns:
        tuple: A tuple containing the full path of the downloaded video and the thumbnail path.
    """

    retry = 0
    while retry < retries:
        try:
            yt = YouTube(youtube_video_url)
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
                logger.warning("Rate limited. Retrying in %s seconds...", wait)
                time.sleep(wait)
                retry += 1
            else:
                logger.error("HTTP error occurred: %s", e)
                return None, None
        except IncompleteRead:
            # Oh well, reconnect and keep trucking
            continue
        except (pytube_exceptions.VideoUnavailable, URLError, ContentTooShortError, RemoteDisconnected, ConnectionError, ChunkedEncodingError) as e:
            logger.warning("Attempt %s failed with error: %s", retry + 1, e)
            if retry < retries - 1:
                sleep_time = backoff_factor * (2 ** retry)
                logger.info("Retrying in %s seconds...", sleep_time)
                time.sleep(sleep_time)
                retry += 1
            else:
                logger.error("Failed to download video after %s attempts.", retries)
                return None, None
        except Exception as e:
            logger.error("An unexpected error occurred: %s", e)
            return None, None
