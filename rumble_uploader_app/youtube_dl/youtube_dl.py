import youtube_dl
from datetime import datetime
from rumble_uploader_app.models import YouTubeVideo

def download_youtube_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title = info_dict.get('title', None)
        video_channel = info_dict.get('channel', None)
        video_description = info_dict.get('description', None)
        video_view_count = info_dict.get('view_count', None)
        video_url = info_dict.get('webpage_url', None)
        video_like_count = info_dict.get('like_count', None)
        video_release_date = info_dict.get('release_date', None)
        video_file_path = ydl.prepare_filename(info_dict)
        video_duration = info_dict.get('duration', None)
        video_upload_date = info_dict.get('upload_date', None)

        # Convert upload_date to a datetime object
        if video_upload_date:
            try:
                video_upload_date = datetime.strptime(video_upload_date, '%Y%m%d').date()
            except ValueError:
                # Handle the ValueError here, for example, by setting video_upload_date to None
                video_upload_date = None

        # Create and save the YouTubeVideo instance
        youtube_video = YouTubeVideo(
            youtube_video_title=video_title,
            youtube_video_description=video_description,
            youtube_video_url=video_url,
            youtube_video_channel= video_channel,
            youtube_view_count= video_view_count,
            youtube_video_likes= video_like_count,
            youtube_video_published_date= video_release_date,
            youtube_video_file=video_file_path,
            youtube_video_duration=video_duration,
            youtube_video_upload_date=video_upload_date
        )
        youtube_video.save()

        return youtube_video
