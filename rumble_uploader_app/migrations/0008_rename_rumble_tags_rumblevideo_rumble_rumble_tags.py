# Generated by Django 5.0.6 on 2024-05-28 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rumble_uploader_app', '0007_rename_youtube_channel_youtubevideo_youtube_video_channel_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rumblevideo',
            old_name='rumble_tags',
            new_name='rumble_rumble_tags',
        ),
    ]
