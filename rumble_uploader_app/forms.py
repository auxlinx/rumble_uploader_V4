from django import forms
from .models import RumbleVideo, YouTubeVideo, YouTubeURL

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
        ('public', 'Public'),
        ('unlisted', 'Unlisted'),
        ('private', 'Private'),
        ('scheduled', 'Scheduled'),
    ]

class RumbleVideoForm(forms.ModelForm):
    """
    Form for Rumble Video.
    """

    def __init__(self, *args, **kwargs):
        super(RumbleVideoForm, self).__init__(*args, **kwargs)

    rumble_primary_category = forms.ChoiceField(choices=PRIMARY_CATEGORY_CHOICES)
    rumble_visibility = forms.ChoiceField(choices=VISIBILITY_CHOICES)

    class Meta:
        model = RumbleVideo
        fields = '__all__'

class YouTubeVideoForm(forms.ModelForm):
    class Meta:
        model = YouTubeVideo
        fields = [
                'youtube_video_url',
                'youtube_video_title',
                'youtube_video_description',
                'youtube_video_channel',
                'youtube_view_count',
                'youtube_video_likes',
                'youtube_video_published_date',
                'youtube_video_upload_date',
                'youtube_video_file',
                'youtube_video_thumbnail'
                  ]
        widgets = {
            'youtube_video_published_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select a date'}),
            'youtube_video_upload_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select a date'}),
        }


class YouTubeURLForm(forms.ModelForm):
    """
    Form for YouTube URL.
    """

    class Meta:
        """
        Meta class for YouTubeURLForm.
        """

        model = YouTubeURL
        fields = [
            'youtube_video_url', 'youtube_video_title', 'youtube_video_description',
            'youtube_video_channel', 'youtube_view_count', 'youtube_video_likes',
            'youtube_video_published_date', 'youtube_video_upload_date', 'youtube_video_file',
            'youtube_video_thumbnail'
        ]
