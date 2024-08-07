# Generated by Django 3.2.25 on 2024-06-26 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rumble_uploader_app', '0018_auto_20240626_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rumblevideo',
            name='rumble_primary_category',
            field=models.CharField(choices=[('auto', 'Auto'), ('cooking', 'Cooking'), ('entertainment', 'Entertainment'), ('finance', 'Finance'), ('gaming', 'Gaming'), ('howto', 'HowTo'), ('music', 'Music'), ('news', 'News'), ('podcasts', 'Podcasts'), ('science', 'Science'), ('sports', 'Sports'), ('technology', 'Technology'), ('travel', 'Travel'), ('viral', 'Viral'), ('vlogs', 'Vlogs')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='rumblevideo',
            name='rumble_visibility',
            field=models.CharField(choices=[('public', 'Public'), ('unlisted', 'Unlisted'), ('private', 'Private'), ('scheduled', 'Scheduled')], max_length=100, null=True),
        ),
    ]
