from libraries.common import log_message, capture_page_screenshot, browser
from libraries.google.google import Google
from libraries.itunes.itunes import Itunes
from config import OUTPUT_FOLDER, tabs_dict


class Process:
    def __init__(self):
        log_message("Initialization")

        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "directory_upgrade": True,
            "download.default_directory": OUTPUT_FOLDER,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False
        }
        browser.open_available_browser(preferences=prefs, browser_selection=["firefox"])
        browser.set_window_size(1920, 1080)
        browser.maximize_browser_window()

    def start(self):
        log_message("Search Movie on Google")
        google = Google(browser, {"url": "https://www.google.com/ncr"})
        tabs_dict["Google"] = len(tabs_dict)
        google.access_google()
        google.search_movie(movie_name="The lord of the Rings: The Return of the King itunes movie us")

        log_message("Extract information from Movie")
        itunes = Itunes(browser)
        del tabs_dict["Google"]
        tabs_dict["itunes"] = len(tabs_dict)
        itunes.extract_information()

        log_message("Write Data as .xlsx on Output Folder")
        itunes.write_data_to_excel()

    def finish(self):
        log_message("DW Process Finished")
        browser.close_browser()
