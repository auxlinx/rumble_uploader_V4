"""
This module scrapes data from YouTube.
"""

import time
import logging
from datetime import datetime
import os
import re
from django.shortcuts import render
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from rumble_uploader_app.forms import YouTubeVideoForm
from .youtube_url_download_script import download_video
from rumble_uploader_app.models import YouTubeVideo

def open_youtube(request):
    """
    Opens the YouTube website using Selenium WebDriver.
    """
    if request.method == 'POST':
        youtube_link = request.POST['youtube_link']
        options = webdriver.ChromeOptions()

        # Add arguments to ChromeOptions to address the issue
        options.add_argument("--headless")  # Run Chrome in headless mode (no GUI).
        options.add_argument("--no-sandbox")  # Bypass OS security model, WARNING: NOT RECOMMENDED FOR PRODUCTION!
        options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems.
        options.add_argument("--remote-debugging-port=9222")  # If you need to connect to the browser for debugging.

        # Ensure ChromeDriver is up-to-date and specify options
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Open YouTube
        driver.get(youtube_link)

        # This will hold all the data we scrape
        data = {}
        # post_copy = request.POST.copy()
        # files_copy = request.FILES.copy()
        try:
            # Wait for the page to load
            time.sleep(5)

            # Extract and print the video URL
            youtube_video_url_element = driver.find_element(By.CSS_SELECTOR, "link[itemprop='url']")
            youtube_video_url = youtube_video_url_element.get_attribute("href")
            data['youtube_video_url'] = youtube_video_url

            # Extract and print the interaction count
            youtube_video_title_element = driver.find_element(By.CSS_SELECTOR, "meta[itemprop='name']")
            youtube_video_title = youtube_video_title_element.get_attribute("content")
            data['youtube_video_title'] = youtube_video_title

            # saved path save_path
            save_path = r'static/media/'

            # Download the url's video
            # download_video(youtube_link, save_path)

            youtube_video_path_relative_path, thumbnail_path_relative_path = download_video(youtube_link, save_path)

            # Use full_path and thumbnail_path as needed
            print(youtube_video_path_relative_path, thumbnail_path_relative_path)

            # Extract and print the upload date
            youtube_video_description_element = driver.find_element(By.CSS_SELECTOR, "meta[itemprop='description']")
            youtube_video_description = youtube_video_description_element.get_attribute("content")
            data['youtube_video_description'] = youtube_video_description

            # Extract and print the author name
            youtube_video_channel_element = driver.find_element(By.CSS_SELECTOR, "span[itemprop='author'] link[itemprop='name']")
            youtube_video_channel = youtube_video_channel_element.get_attribute("content")
            data['youtube_video_channel'] = youtube_video_channel

            # Extract and print the interaction count
            youtube_video_interaction_count_element = driver.find_element(
                By.CSS_SELECTOR,
                "meta[itemprop='interactionCount']"
            )
            youtube_view_count = youtube_video_interaction_count_element.get_attribute("content")
            data['youtube_view_count'] = youtube_view_count

            # Assuming the likes are in a button with an aria-label attribute that contains the likes count
            likes_element = driver.find_element(By.XPATH, "//button[@aria-label[contains(., 'like')]]")
            likes_count = likes_element.get_attribute("aria-label")

            # Process the likes_count to extract just the numerical part if necessary
            likes_count_numeric = re.findall(r'\d+', likes_count.replace(',', ''))  # Removes commas and extracts numbers
            likes_count_numeric = int(likes_count_numeric[0]) if likes_count_numeric else 0  # Default to 0 if not found

            data['youtube_video_likes'] = likes_count_numeric

            # Extract and print the upload date
            youtube_video_upload_date_element = driver.find_element(By.CSS_SELECTOR, "meta[itemprop='uploadDate']")
            youtube_video_upload_date = youtube_video_upload_date_element.get_attribute("content")

            # Convert the string to a datetime object
            youtube_video_upload_date_obj = datetime.strptime(youtube_video_upload_date, '%Y-%m-%dT%H:%M:%S%z')

            # Assign the datetime object directly
            data['youtube_video_upload_date'] = youtube_video_upload_date_obj

            # Extract and print the published date
            youtube_video_published_date_element = driver.find_element(By.CSS_SELECTOR, "meta[itemprop='datePublished']")
            youtube_video_published_date = youtube_video_published_date_element.get_attribute("content")

            # Convert the string to a datetime object
            youtube_video_published_date_obj = datetime.strptime(youtube_video_published_date, '%Y-%m-%dT%H:%M:%S%z')

            # Assign the datetime object directly
            data['youtube_video_published_date'] = youtube_video_published_date_obj

            data['youtube_video_file'] = youtube_video_path_relative_path
            data['youtube_video_thumbnail'] = thumbnail_path_relative_path
            # print(data)
            driver.quit()  # Ensure the driver is closed in the end


         # Save paths to YouTubeVideo model
            youtube_video = YouTubeVideo.objects.create(**data)
            youtube_video.save()
            # Assuming you have a template to show success
            try:
                # Include a success message in the context
                context = {
                    'data': data,
                    'success_message': 'YouTube video uploaded successfully! Upload another?'
                }
                return render(request, 'url/youtube_url_upload.html', context)
            except Exception as e:
                logging.error("Error rendering template: %s", e)
                return JsonResponse({'error': 'Error rendering template'}, status=500)

        except NoSuchElementException as e:
            logging.error("Element not found: %s", e)
            return JsonResponse({'error': 'Element not found'}, status=404)
        except ValueError as e:
            # If an error occurs, close the driver and return an error message
            driver.quit()
            return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            logging.error("An unexpected error occurred: %s", e)
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
