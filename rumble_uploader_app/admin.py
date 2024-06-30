"""
Module docstring goes here.
"""

from django.contrib import admin
from .models import RumbleVideo, YouTubeVideo, YouTubeURL

# Register your models here.
class RumbleVideoAdmin(admin.ModelAdmin):
    """
    Class docstring goes here.
    """
    fieldsets = (
        ('Video Information', {
            'fields': (
                'rumble_video_title', 'rumble_video_description', 'rumble_video_url', 'rumble_primary_category',
                'rumble_secondary_category', 'rumble_rumble_tags', 'rumble_visibility', 'rumble_video_file', 'rumble_thumbnail'
            )
        }),
    )
    list_display = ('rumble_video_title', 'rumble_upload_date')
    search_fields = ['rumble_video_title', 'rumble_video_description']
    list_filter = ['rumble_upload_date']
    list_per_page = 10

class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ('youtube_video_title', 'youtube_video_channel', 'youtube_video_published_date')
    search_fields = ('youtube_video_title', 'youtube_video_channel')
    list_filter = ('youtube_video_title', 'youtube_video_published_date')

class YouTubeURLAdmin(admin.ModelAdmin):
    list_display = ('youtube_video_url',)
    search_fields = ('youtube_video_url',)
    list_filter = ('youtube_video_url',)


admin.site.register(YouTubeURL, YouTubeURLAdmin)
admin.site.register(YouTubeVideo, YouTubeVideoAdmin)
admin.site.register(RumbleVideo, RumbleVideoAdmin)
