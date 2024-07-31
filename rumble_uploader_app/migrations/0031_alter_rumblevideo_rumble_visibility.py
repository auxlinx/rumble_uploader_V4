# Generated by Django 3.2.25 on 2024-07-31 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rumble_uploader_app', '0030_alter_youtubevideo_youtube_video_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rumblevideo',
            name='rumble_visibility',
            field=models.CharField(choices=[('private', 'Private'), ('public', 'Public'), ('unlisted', 'Unlisted'), ('scheduled', 'Scheduled')], default='Private', max_length=100, null=True),
        ),
    ]