# Generated by Django 3.2.25 on 2024-07-17 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rumble_uploader_app', '0025_alter_rumblevideo_rumble_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youtubeurl',
            name='youtube_video_channel',
        ),
        migrations.RemoveField(
            model_name='youtubeurl',
            name='youtube_video_description',
        ),
        migrations.RemoveField(
            model_name='youtubeurl',
            name='youtube_video_downloaded',
        ),
        migrations.RemoveField(
            model_name='youtubeurl',
            name='youtube_video_file',
        ),
        migrations.RemoveField(
            model_name='youtubeurl',
            name='youtube_video_likes',
        ),
        migrations.RemoveField(
            model_name='youtubeurl',
            name='youtube_video_published_date',
        ),
        migrations.RemoveField(
            model_name='youtubeurl',
            name='youtube_video_thumbnail',
        ),
        migrations.RemoveField(
            model_name='youtubeurl',
            name='youtube_video_title',
        ),
        migrations.RemoveField(
            model_name='youtubeurl',
            name='youtube_video_upload_date',
        ),
        migrations.RemoveField(
            model_name='youtubeurl',
            name='youtube_view_count',
        ),
    ]
