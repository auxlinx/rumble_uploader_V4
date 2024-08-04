"""
This module is responsible for running the rumble uploader test.
"""
import sys
import os
from rumble_uploader_app.rumble_uploader_script.rumble_uploader import upload_to_rumble

# Add the parent directory of rumble_uploader_app to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# sys.path.append(r'D:\Proton Drive Backup\rahw_coding_mobile\aux_coding\rumble_uploader\rumble_uploader_V4\rumble_uploader_app')

test_rumble_video_script_data = ({
            "rumble_account": "randomrumblevideos",
            "videoTitle": "test",
            "videoDescription": "test",
            "video_tags": "test",
            "video_category": "test",
            "video_secondary_category": "test",
            "rumble_video_file": "videos/test.mp4",
            "rumble_video_visibility_setting": "Private",
            "rumble_video_licensing_setting": "Rumble Video Management Exclusive",
        })


# Call the function
upload_to_rumble(test_rumble_video_script_data, headless=False)
