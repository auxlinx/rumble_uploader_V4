from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# from .views import open_youtube  # Adjust the import path according to your project structure


from rumble_uploader_app.views import ( home,
    #  Display IP address
    display_ip_address,
    #    Rumble videos
    rumble_upload_video,
    rumble_video_list,
    rumble_video_detail,
    rumble_video_delete,
    rumble_video_update,
    # Youtube videos
    youtube_to_rumble_conversion_list,
    youtube_upload_video,
    youtube_video_list,
    youtube_video_detail,
    youtube_video_delete,
    youtube_video_update,
    convert_video,
    # Urls for youtube urls
    youtube_url_upload,
    youtube_url_add,
    youtube_url_detail,
    youtube_url_list,
    youtube_url_delete,
    youtube_url_update,
    file_upload_view,
    download_view,
    # open_youtube,
    error_view,
    # Scripts
    run_rumble_script,
    upload_all_videos_to_rumble,
    scrape_youtube,
    )

urlpatterns = [
    # Admin
    path('upload/', file_upload_view, name='file_upload'),
    path('download/', download_view, name='file_download'),
    path('error/', error_view, name='error_view'),
    path('show-ip/', display_ip_address, name='show_ip'),
    #  Home
    path('', home, name='home'),
    # youtube url
    path('youtube_url_upload', youtube_url_upload, name='youtube_url_upload'),
    path('youtube_urls/', youtube_url_list, name='youtube_url_list'),
    path('youtube_url/<int:pk>/', youtube_url_detail, name='youtube_url_detail'),
    # path('scrape_youtube/', open_youtube, name='scrape_youtube'),
    # path('youtube_url/<int:pk>/', youtube_url_scrape_detail, name='youtube_url_scrape_detail'),
    path('youtube_url/<int:pk>/delete/', youtube_url_delete, name='youtube_url_delete'),
    path('youtube_url/<int:pk>/update/', youtube_url_update, name='youtube_url_update'),
    # rumble video urls
    path('rumble_upload/', rumble_upload_video, name='rumble_upload_video'),
    path('rumble_videos/', rumble_video_list, name='rumble_video_list'),
    path('rumble_video/<int:pk>/', rumble_video_detail, name='rumble_video_detail'),
    path('rumble_video/<int:pk>/delete/', rumble_video_delete, name='rumble_video_delete'),
    path('rumble_video/<int:pk>/update/', rumble_video_update, name='rumble_video_update'),
    path('youtube_to_rumble_conversion/', youtube_to_rumble_conversion_list, name='youtube_to_rumble_conversion_list'),
    # youtube video urls
    path('youtube_upload_video/', youtube_upload_video, name='youtube_upload_video'),
    path('youtube_url_add/', youtube_url_add, name='youtube_url_add'),
    path('youtube_video_list/', youtube_video_list, name='youtube_video_list'),
    path('youtube_video/<int:pk>/', youtube_video_detail, name='youtube_video_detail'),
    path('youtube_video/<int:pk>/delete/', youtube_video_delete, name='youtube_video_delete'),
    path('youtube_video/<int:pk>/update/', youtube_video_update, name='youtube_video_update'),
    path('convert-video/<int:youtube_video_pk>', convert_video, name='convert_video'),
    # script running url
    path('run_rumble_script/<int:pk>/', run_rumble_script, name='run_rumble_script'),
    path('scrape_youtube/', scrape_youtube, name='scrape_youtube'),
    path('upload-videos/', upload_all_videos_to_rumble, name='upload_videos'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
