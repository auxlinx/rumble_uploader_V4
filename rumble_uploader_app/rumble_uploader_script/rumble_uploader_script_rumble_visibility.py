# Rumble video visibility settings
from .rumble_uploader_script_html_elements import (
    visibility_option_selector_private,
    visibility_option_selector_public,
    visibility_option_selector_unlisted)

def rumble_visibility(visibility_setting):
    video_visibility_option_selection = None

    if visibility_setting == "Private":
        video_visibility_option_selection = visibility_option_selector_private
    elif visibility_setting == "Public":
        video_visibility_option_selection = visibility_option_selector_public
    elif visibility_setting == "Unlisted":
        video_visibility_option_selection = visibility_option_selector_unlisted
    return video_visibility_option_selection
