from libraries.common import act_on_element, capture_page_screenshot, log_message, check_file_download_complete, files
from config import OUTPUT_FOLDER


class Itunes:

    def __init__(self, rpa_selenium_instance, credentials: dict):
        self.browser = rpa_selenium_instance
        self.data_dict_list = []

    def extract_information(self):
        """
        Extract information from itunes website.
        """
        pass

    def write_data_to_excel(self):
        """
        Writes the data extracted to an excel file
        """
        pass

