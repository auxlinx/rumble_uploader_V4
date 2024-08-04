"""
This module is responsible for running the rumble uploader test.
"""
from rumble_uploader_app.Tests.rumble_uploader_test import upload_to_rumble

# sys.path.append(r'D:\Proton Drive Backup\rahw_coding_mobile\aux_coding\rumble_uploader\rumble_uploader_V4\rumble_uploader_app')

test_rumble_video_script_data = ({
            "rumble_account": "rumblevideos",
            "videoTitle": "test",
            "videoDescription": "test",
            "videoTags": "test",
            "videoCategory": "test",
            "rumble_video_visibility": "Private",
            "videoSecondCategory": "test",
            "rumble_video_file": "videos/test.mp4",
        })


# Call the function
upload_to_rumble(test_rumble_video_script_data)
