"""
This module is responsible for running the rumble uploader test.
"""
import unittest
import sys
import os

from rumble_uploader_app.rumble_uploader_script.rumble_uploader import upload_to_rumble

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


class TestUploadToRumble(unittest.TestCase):
    def test_upload_to_rumble_headless_false(self):
        # Define the test data
        test_rumble_video_script_data = {
            "rumble_account": "randomrumblevideos",
            "videoTitle": "test",
            "videoDescription": "test",
            "video_tags": "test",
            "video_category": "test",
            "video_secondary_category": "test",
            "rumble_video_file": "videos/test.mp4",
            "rumble_video_visibility_setting": "Private",
            "rumble_video_licensing_setting": "Rumble Video Management Exclusive",
        }

        # Call the function with headless=False
        upload_to_rumble(test_rumble_video_script_data, headless=False)

        # Add assertions here to verify the expected behavior
        # For example, you can check if certain files were created or certain logs were generated
        # This is a placeholder as the actual assertions will depend on the function's behavior
        # self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
