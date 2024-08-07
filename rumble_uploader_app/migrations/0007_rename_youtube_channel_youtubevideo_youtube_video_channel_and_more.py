# Generated by Django 5.0.6 on 2024-05-28 14:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rumble_uploader_app', '0006_youtubevideo_youtube_video_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='youtubevideo',
            old_name='youtube_channel',
            new_name='youtube_video_channel',
        ),
        migrations.RenameField(
            model_name='youtubevideo',
            old_name='youtube_video_posted_date',
            new_name='youtube_video_published_date',
        ),
        migrations.RemoveField(
            model_name='youtubeurl',
            name='youtube_url',
        ),
        migrations.AddField(
            model_name='youtubeurl',
            name='youtube_video_channel',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='youtubeurl',
            name='youtube_video_description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='youtubeurl',
            name='youtube_video_likes',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='youtubeurl',
            name='youtube_video_published_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='youtubeurl',
            name='youtube_video_title',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='youtubeurl',
            name='youtube_video_upload_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='youtubeurl',
            name='youtube_video_url',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='youtubeurl',
            name='youtube_view_count',
            field=models.BigIntegerField(null=True),
        ),
    ]
