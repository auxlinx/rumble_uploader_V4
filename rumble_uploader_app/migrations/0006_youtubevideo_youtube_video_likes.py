# Generated by Django 3.2.25 on 2024-05-28 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rumble_uploader_app', '0005_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubevideo',
            name='youtube_video_likes',
            field=models.BigIntegerField(null=True),
        ),
    ]
