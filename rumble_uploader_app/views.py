"""
Module docstring describing the purpose of the module.
"""
import subprocess
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import Http404, JsonResponse, HttpResponseRedirect,FileResponse, HttpResponseBadRequest,HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from rumble_uploader_app.templates.rumble_videos.rumble_video_options import rumble_video_primary_categories, rumble_accounts, rumble_video_secondary_categories, rumble_video_visibility
import logging
# from .rumble_uploader import process_and_return_link
logger = logging.getLogger(__name__)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import YouTubeVideoSerializer, RumbleVideoSerializer
from .forms import RumbleVideoForm, YouTubeVideoForm, YouTubeURLForm
from .models import RumbleVideo, YouTubeVideo, YouTubeURL
from .youtube_url_download_script import download_video
from .youtube_url_scrape_script import open_youtube
from .youtube_to_rumble_converter import convert_youtube_video_to_rumble
from rumble_uploader_app.rumble_uploader import upload_to_rumble

# Load the .env file
load_dotenv()

#  Admin
@api_view(['POST'])
def file_upload_view(request):
    """
    Function docstring describing the purpose of the function.
    """
    if request.method == 'POST':
        file_serializer = YouTubeVideoSerializer(data=request.data)
        file_serializer = RumbleVideoSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def download_view(request, file_path):
    try:
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    except FileNotFoundError as exc:
        raise Http404() from exc

# Errors

def error_view(request, error_message="An unexpected error occurred"):
    """
    Render the error page with an optional error message.
    """
    context = {'error': error_message}
    return render(request, 'admin/error_template.html', context)

# Home page view
def home(request):
    current_datetime = datetime.now()
    return render(request, 'home.html', {'current_datetime': current_datetime})

# rumble video views

def rumble_upload_video(request):
    if request.method == 'POST':
        form = RumbleVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)
            return render(request, 'rumble_videos/rumble_video_uploader.html', {'form': form})

    else:
        form = RumbleVideoForm()

    return render(request, 'rumble_videos/rumble_video_uploader.html', {'form': form})


def rumble_video_list(request):
    """
    Function docstring describing the purpose of the function.
    """
    rumble_videos = RumbleVideo.objects.all()
    return render(request, 'rumble_videos/rumble_video_list.html', {'rumble_videos': rumble_videos})

def youtube_to_rumble_conversion_list(request):
    """
    Function docstring describing the purpose of the function.
    """
    # Assuming your .env has a variable like RUMBLE_CHANNELS=Channel1,Channel2,Channel3
    context = {'rumble_video_primary_categories': rumble_video_primary_categories,
               'rumble_video_secondary_categories': rumble_video_secondary_categories,
               "rumble_video_visibility": rumble_video_visibility,
               'rumble_accounts': rumble_accounts,
               'rumble_videos': RumbleVideo.objects.all(),
               'youtube_videos': YouTubeVideo.objects.all()}
    return render(request, 'youtube_videos/youtube_video_conversion_list.html', context)


def convert_video(request):
    """
    Convert a YouTube video to a Rumble video.
    """
    if request.method == 'POST':
        youtube_video_pk = request.POST.get('youtube_video_pk')  # Adjust the field name as necessary
        youtube_video = get_object_or_404(YouTubeVideo, pk=youtube_video_pk)
        # Proceed with your conversion logic

        # Log POST and FILES data
        logger.debug('POST data: %s', request.POST)
        logger.debug('FILES data: %s', request.FILES)
        # Use get_object_or_404 to simplify object retrieval and 404 handling


        # Step 2: Retrieve POST Data
        # Example: Getting title and description from POST data, adjust according to your form fields
        input_rumble_account = request.POST.get('rumble_accounts')  # Default to YouTube video title if not provided
        input_rumble_video_primary_categories = request.POST.get('rumble_video_primary_categories')  # Default to YouTube video title if not provided
        input_rumble_video_secondary_categories = request.POST.get('rumble_video_secondary_categories')  # Default to YouTube video description if not provided
        input_rumble_tags = request.POST.get('rumble_tags')  # Default to YouTube video description if not provided
        input_rumble_video_visibility = request.POST.get('rumble_video_visibility')  # Default to YouTube video description if not provided

        # Step 3: Create New Rumble Video
        new_rumble_video = RumbleVideo(
            # Set fields based on youtube_video_data and input
            rumble_account = input_rumble_account,
            rumble_video_title= youtube_video.youtube_video_title,
            rumble_video_description = youtube_video.youtube_video_description,
            rumble_video_url = youtube_video.youtube_video_url,
            rumble_primary_category = input_rumble_video_primary_categories,
            rumble_secondary_category = input_rumble_video_secondary_categories,
            rumble_rumble_tags = input_rumble_tags,
            rumble_upload_date = youtube_video.youtube_video_upload_date,
            rumble_visibility = input_rumble_video_visibility,
            rumble_video_file = youtube_video.youtube_video_file,
            rumble_thumbnail = youtube_video.youtube_video_thumbnail
            # Set other fields as needed, possibly using youtube_video data
        )

        # Step 4: Save the New Rumble Video
        new_rumble_video.save()

        # Return a response, e.g., redirect or JSON response
        return redirect('rumble_video_list')

def rumble_video_detail(request, pk):
    rumble_video = get_object_or_404(RumbleVideo, pk=pk)
    return render(request, 'rumble_videos/rumble_video_detail.html', {'rumble_video': rumble_video})

def rumble_video_delete(request, pk):
    # Attempt to retrieve the video to be deleted
    rumble_video = get_object_or_404(RumbleVideo, pk=pk)

    if request.method == 'POST':
        # Delete the video and redirect to the video list
        rumble_video.delete()
        # Optionally, you can add a success message here
        messages.success(request, "Video was successfully deleted.")
        return redirect('rumble_video_list')  # Assuming you have a URL named 'rumble_video_list'
    else:
        # If not a POST request, render a confirmation page or redirect
        # For simplicity, we're redirecting directly here
        return render(request, 'rumble_videos/rumble_video_list.html')

def rumble_video_update(request, pk):
    rumble_video = get_object_or_404(RumbleVideo, pk=pk)  # Fetch the video instance
    if request.method == 'POST':
        # Initialize form with POST data, FILES (if your form includes file upload), and the existing video instance for update
        update_form = RumbleVideoForm(request.POST, request.FILES, instance=rumble_video)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Video was successfully updated.")  # Optionally, add a success message
            return redirect('rumble_video_list')  # Redirect to the video list or detail view
    else:
        # For a GET request, initialize the form with the instance to pre-fill the form fields
        update_form = RumbleVideoForm(instance=rumble_video)

    # Render the form in both GET and POST requests
    return render(request, 'rumble_videos/rumble_video_update.html', {'update_form': update_form})

# youtube url

def youtube_url_upload(request):
    if request.method == 'POST':
        form = YouTubeURLForm(request.POST)
        if form.is_valid():
            youtube_url = form.cleaned_data.get('youtube_url')
            save_path = "D:\\Proton Drive\\My files\\rahw_coding_mobile\\aux_coding\\rumble_uploader\\rumble_upload_test_video"
            download_success = download_video(youtube_url, save_path)
            if download_success:
                form.save()
                return redirect('youtube_url_upload')
            else:
                form.add_error(None, "Failed to download video.")
    else:
        form = YouTubeURLForm()
    return render(request, 'url/youtube_url_upload.html', {'form': form})


def youtube_url_add(request):
    """
    Function docstring describing the purpose of the function.
    """
    if request.method == 'POST':
        form = YouTubeVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('youtube_url_list')
        else:
            print(form.errors)
            return render(request, 'url/youtube_url_add_form.html', {'form': form})
    else:
        form = YouTubeVideoForm()
    return render(request, 'url/youtube_url_add_form.html', {'form': form})

def youtube_url_detail(request, pk):
    youtube_url = get_object_or_404(YouTubeURL, pk=pk)
    return render(request, 'url/youtube_url_detail.html', {'youtube_url': youtube_url})

def youtube_url_list(request):
    youtube_urls = YouTubeURL.objects.all()
    return render(request, 'url/youtube_url_list.html', {'youtube_urls': youtube_urls})

def youtube_url_delete(request, pk):
    youtube_url = YouTubeURL.objects.get(pk=pk)
    youtube_url.delete()
    messages.success(request, 'URL deleted successfully')
    return redirect(reverse('url/youtube_url_list'))


def youtube_url_update(request, pk):
    youtube_url = get_object_or_404(YouTubeURL, pk=pk)
    if request.method == 'POST':
        form = YouTubeURLForm(request.POST, instance=youtube_url)
        if form.is_valid():
            form.save()
            return redirect('youtube_url_detail.html', pk=youtube_url.pk)
    else:
        form = YouTubeURLForm(instance=youtube_url)
    return render(request, 'url/youtube_url_update.html', {'form': form})

# youtube video views


def youtube_upload_video(request):
    """
    Function docstring describing the purpose of the function.
    """
    if request.method == 'POST':
        form = YouTubeVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = YouTubeVideoForm()
    return render(request, 'youtube_videos/youtube_video_uploader.html', {'form': form})


def youtube_video_list(request):
    """
    Function docstring describing the purpose of the function.
    """
    youtube_videos = YouTubeVideo.objects.all()
    return render(request, 'youtube_videos/youtube_video_list.html', {'youtube_videos': youtube_videos})


def youtube_video_detail(request, pk):
    youtube_video = get_object_or_404(YouTubeVideo, pk=pk)
    return render(request, 'youtube_videos/youtube_video_detail.html', {'youtube_video': youtube_video})


def youtube_video_delete(request, pk):
    video = YouTubeVideo.objects.get(pk=pk)
    video.delete()
    messages.success(request, 'Video deleted successfully')
    return redirect(reverse('youtube_video_list'))


def youtube_video_update(request, pk):

    youtube_video = get_object_or_404(YouTubeVideo, pk=pk)  # Fetch the video instance
    if request.method == 'POST':
        # Initialize form with POST data, FILES (if your form includes file upload), and the existing video instance for update
        update_form = YouTubeVideoForm(request.POST, request.FILES, instance=youtube_video)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Video was successfully updated.")  # Optionally, add a success message
            return redirect('youtube_video_list')  # Redirect to the video list or detail view
    else:
        # For a GET request, initialize the form with the instance to pre-fill the form fields
        update_form = YouTubeVideoForm(instance=youtube_video)

    # Render the form in both GET and POST requests
    return render(request, 'youtube_videos/youtube_video_update.html', {'update_form': update_form})


# script run views

def run_rumble_script(request, pk):

    rumble_video = get_object_or_404(RumbleVideo, pk=pk)
    if request.method == 'POST':
        rumble_video_data = RumbleVideo.objects.get(pk=pk)
        rumble_video_absolute_path = rumble_video.rumble_video_file.name
        # base_dir = Path(r"C:\Users\auxil\Documents\rumble_script V3\static\media")
        # relative_path = rumble_video.rumble_video_file.name.lstrip("/")
        # absolute_path = base_dir / relative_path.replace("/", "\\")
        # rumble_video_absolute_path = str(absolute_path)
        # print(rumble_video_absolute_path)
        # "C:\Users\auxil\Documents\rumble_script V3\static\media\videos\Deadpool&Wolverine-OldBubs.mp4"

        rumble_video_script_data = ({
            "pk": rumble_video.pk,
            "videoTitle": rumble_video.rumble_video_title,
            "videoDescription": rumble_video.rumble_video_description,
            "videoTags": rumble_video.rumble_rumble_tags,
            "videoCategory": rumble_video.rumble_primary_category,
            "videoSecondCategory": rumble_video.rumble_secondary_category,
            "rumble_video_file": rumble_video_absolute_path,
        })
        # print(rumble_video_script_data)
        # Serialize to JSON
        try:
            # Attempt to parse the JSON string
            rumble_video_script_serialized_data = json.dumps(rumble_video_script_data)
            print("The string is properly formatted as JSON.")
        except json.JSONDecodeError as e:
            # If an error occurs, the string is not properly formatted as JSON
            print(f"The string is not properly formatted as JSON: {e}")
        # print(rumble_video_script_serialized_data)
        upload_to_rumble(rumble_video_script_serialized_data)
        # print(rumble_video_detail)
        # print(rumble_video_links_json_data)
        video_links_data = process_and_return_link
        print(video_links_data)

    # return JsonResponse(rumble_video_links_json_data)



@require_http_methods(["POST"])
def scrape_youtube_view(request):
    """
    Scrape YouTube information, save it to the database, and return the data as a JSON response.
    """
    form = YouTubeVideoForm(request.POST, request.FILES)
    if form.is_valid():
        query = form.cleaned_data['query']
        try:
            data = open_youtube(query)  # Assume this returns data suitable for creating/updating a YouTubeVideo instance
            # Assuming 'data' is a dictionary with keys matching YouTubeVideo model fields
            video, created = YouTubeVideo.objects.update_or_create(
                query=query,
                defaults=data,
            )
            # Optionally, convert the video instance to a dictionary to return as JSON
            video_data = YouTubeVideoForm(video)
            return JsonResponse(video_data)
        except NoSuchElementException as e:  # Corrected exception
            # Log the error here if needed
            return JsonResponse({'error': 'Failed to scrape YouTube.', 'details': str(e)}, status=500)
    else:
        return HttpResponseBadRequest("Invalid input.")
