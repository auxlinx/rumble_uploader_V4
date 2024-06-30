# Generated by Django 5.0.6 on 2024-05-24 14:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rumble_uploader_app', '0003_youtubeurl_youtube_video_date_downloaded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubeurl',
            name='youtube_video_date_downloaded',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='youtubeurl',
            name='youtube_video_downloaded',
            field=models.FileField(blank=True, null=True, upload_to='D:\\Proton Drive\\My files\\rahw_coding_mobile\\aux_coding\\rumble_uploader\\rumble_upload_test_video'),
        ),
    ]
