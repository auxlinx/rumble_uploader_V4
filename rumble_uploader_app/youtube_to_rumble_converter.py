from .models import YouTubeVideo, RumbleVideo
from django.shortcuts import get_object_or_404
from django.http import HttpRequest  # For type annotation



def convert_youtube_video_to_rumble(request: HttpRequest, youtube_video_pk, input_rumble_video_primary_categories, input_rumble_video_secondary_categories, input_rumble_rumble_tags, input_rumble_video_visibility):
    if request.method == 'POST':
            # Fetch the YouTube video from the database
            youtube_video = get_object_or_404(YouTubeVideo, pk=youtube_video_pk)

            # Create a new RumbleVideo instance
            new_rumble_video = RumbleVideo()

            # Set fields based on youtube_video_data and input
            new_rumble_video.rumble_video_description = youtube_video.youtube_video_description
            new_rumble_video.rumble_video_url = youtube_video.youtube_video_url
            new_rumble_video.rumble_primary_category = input_rumble_video_primary_categories
            new_rumble_video.rumble_secondary_category = input_rumble_video_secondary_categories
            new_rumble_video.rumble_rumble_tags = input_rumble_rumble_tags
            new_rumble_video.rumble_upload_date = youtube_video.youtube_video_upload_date
            new_rumble_video.rumble_visibility = input_rumble_video_visibility
            new_rumble_video.rumble_video_file = youtube_video.youtube_video_file
            new_rumble_video.rumble_thumbnail = youtube_video.youtube_video_thumbnail

            # Save the instance to be able to add ManyToMany relations
            new_rumble_video.save()

            print(new_rumble_video.rumble_primary_category)


    return new_rumble_video
