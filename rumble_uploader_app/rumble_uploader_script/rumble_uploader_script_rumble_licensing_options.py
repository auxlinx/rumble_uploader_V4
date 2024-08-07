# Rumble video visibility settings
from .rumble_uploader_script_html_elements import (
    rumble_video_management_button_exclusive_selector,
    rumble_video_management_button_non_exclusive_selector,
    rumble_video_management_button_rumble_only_selector)
# Rumble video visibility settings
def rumble_licensing_options(licensing_options):
    rumble_licensing_options_selection = None

    if licensing_options == "Rumble Video Management Exclusive":
        rumble_licensing_options_selection= rumble_video_management_button_exclusive_selector
    elif licensing_options == "Rumble Video Management Non Exclusive":
        rumble_licensing_options_selection= rumble_video_management_button_non_exclusive_selector
    elif licensing_options == "Rumble Video Management Rumble Only":
        rumble_licensing_options_selection= rumble_video_management_button_rumble_only_selector
    return rumble_licensing_options_selection
