# Generated by Django 3.2.25 on 2024-05-24 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rumble_uploader_app', '0002_youtubeurl_youtube_video_downloaded'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubeurl',
            name='youtube_video_date_downloaded',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
