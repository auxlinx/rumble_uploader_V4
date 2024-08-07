# Generated by Django 3.2.25 on 2024-07-12 12:14

from django.db import migrations, models
import rumble_uploader_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('rumble_uploader_app', '0023_alter_rumblevideo_rumble_video_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rumblevideo',
            name='rumble_direct_link',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rumblevideo',
            name='rumble_embed_code',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rumblevideo',
            name='rumble_monetized_embed',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rumblevideo',
            name='rumble_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails/', validators=[rumble_uploader_app.models.validate_image_type]),
        ),
    ]
