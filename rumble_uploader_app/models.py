from datetime import datetime
import os
# import re
from django.db import models
# from selenium import webdriver
from django.utils import timezone
# from datetime import datetime
from django.core.exceptions import ValidationError
# from django.utils.text import slugify


# def sanitize_filename(value):
#     # Remove invalid file name characters
#     sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', value)
#     # Replace spaces or other undesired characters
#     sanitized = re.sub(r'[^\w\s-]', '', sanitized).strip()
#     sanitized = re.sub(r'[-\s]+', '-', sanitized)
#     # Truncate to 100 characters
#     sanitized = sanitized[:100]
#     if not sanitized:
#         raise ValidationError("Invalid filename.")
#     return sanitized

def validate_file_type(upload):
    # Example validation: check file extension
    valid_extensions = ['.mp4', '.avi', '.mov', '.flv']
    extension = os.path.splitext(upload.name)[1]
    if extension.lower() not in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

def validate_image_type(upload):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    extension = os.path.splitext(upload.name)[1]
    if extension.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension for image.')

def dynamic_upload_path(instance, filename):
    # Example: organize files by upload date
    return 'videos/{0}/{1}'.format(datetime.now().strftime('%Y/%m/%d'), filename)


class Document(models.Model):
    uploaded_file = models.FileField(upload_to='documents/')


PRIMARY_CATEGORY_CHOICES = [
        ('auto', 'Auto'),
        ('cooking', 'Cooking'),
        ('entertainment', 'Entertainment'),
        ('finance', 'Finance'),
        ('gaming', 'Gaming'),
        ('howto', 'HowTo'),
        ('music', 'Music'),
        ('news', 'News'),
        ('podcasts', 'Podcasts'),
        ('science', 'Science'),
        ('sports', 'Sports'),
        ('technology', 'Technology'),
        ('travel', 'Travel'),
        ('viral', 'Viral'),
        ('vlogs', 'Vlogs'),
    ]

VISIBILITY_CHOICES = [
        ('private', 'Private'),
        ('public', 'Public'),
        ('unlisted', 'Unlisted'),
        ('scheduled', 'Scheduled'),
    ]

RUMBLE_ACCOUNT_CHOICES = [
    ("randomrumblevideos", "randomrumblevideos"),
    ("rumblearchives", "rumblearchives"),
    ("therumblewarfootage", "therumblewarfootage"),
]

class RumbleVideo(models.Model):
    rumble_account = models.CharField(max_length=200, null=True, blank=True, choices=RUMBLE_ACCOUNT_CHOICES)
    rumble_video_title = models.CharField(max_length=200)
    rumble_video_description = models.TextField(null=True)
    rumble_video_url = models.URLField(max_length=200, null=True, blank=True)
    rumble_primary_category = models.CharField(max_length=200, null=True, choices=PRIMARY_CATEGORY_CHOICES)
    rumble_secondary_category = models.CharField(max_length=200, null=True)
    rumble_rumble_tags = models.CharField(max_length=200, null=True)
    rumble_upload_date = models.DateTimeField(auto_now_add=True, null=True)
    rumble_visibility = models.CharField(max_length=100, null=True, choices=VISIBILITY_CHOICES, default='Private')
    rumble_video_file = models.FileField(upload_to='videos/', null=True)
    rumble_thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True, validators=[validate_image_type])
    rumble_direct_link = models.TextField(null=True, blank=True)
    rumble_embed_code = models.TextField(null=True, blank=True)
    rumble_monetized_embed = models.TextField(null=True, blank=True)
    uploaded_to_rumble_success = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return str(self.rumble_video_title)

class YouTubeVideo(models.Model):
    youtube_video_url = models.URLField(max_length=200, null=True)
    youtube_video_title = models.CharField(max_length=200)
    youtube_video_description = models.TextField(null=True)
    youtube_video_channel = models.TextField(null=True)
    youtube_view_count = models.BigIntegerField(null=True)
    youtube_video_likes = models.BigIntegerField(null=True)
    youtube_video_published_date = models.DateField(null=True)
    youtube_video_upload_date = models.DateTimeField(null=True)
    youtube_video_file = models.FileField(
        upload_to='videos/',
        validators=[validate_file_type],
        null=True
    )
    youtube_video_thumbnail = models.FileField(
        upload_to='thumbnails/',
        validators=[validate_image_type],
        null=True,
        blank=True
    )
    objects = models.Manager()

    def __str__(self):
        return str(self.youtube_video_title)

class YouTubeURL(models.Model):
    """
    Represents a YouTube URL.
    """
    youtube_video_url = models.URLField(max_length=200, null=True)
    youtube_video_title = models.CharField(max_length=200, default="Default Title")
    youtube_video_downloaded_successfully = models.BooleanField(default=False)
    objects = models.Manager()
    def __str__(self):
        return str(self.youtube_video_title)
