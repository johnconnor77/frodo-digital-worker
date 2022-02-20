from libraries.common import act_on_element, capture_page_screenshot, log_message, check_file_download_complete, files
from config import OUTPUT_FOLDER


class Itunes:

    def __init__(self, rpa_selenium_instance, url: str = 'https://itunes.apple.com'):
        self.browser = rpa_selenium_instance
        self.itunes_url = url
        self.data_dict = {}
        self.data_dict_list = []

    def access_itunes(self):
        self.browser.go_to(self.itunes_url)

    def extract_information(self):
        """
        Extract information from itunes website.
        """
        data_dict_list = []
        data_dict = {}

        data_rows = act_on_element('//div[@class="l-row cast-list"]/dl//dd', "find_elements")

        for data_row in data_rows:
            artist_name = data_row.find_element_by_xpath('./a').text
            if artist_name in data_dict:
                continue
            else:
                data_dict[artist_name] = data_row.find_element_by_xpath('./a').get_attribute('href')

        self.browser.execute_javascript("window.open()")
        self.browser.switch_window(locator="NEW")

        for key, value in data_dict.items():
            print(key)
            self.itunes_url = value
            self.access_itunes()
            data_columns = act_on_element(
                '//section[@class="l-content-width section section--bordered"]/div/h2[text()="Movies"]/parent::div//following-sibling::div//div[@class="we-lockup__text"]',
                "find_elements", time_range=8)
            movies_genres_list = []

            for data_column in data_columns:
                movie_genre = data_column.text.split("\n")
                movies_genres_list.append(movie_genre)

            data_dict_list.append({key: movies_genres_list})

        self.browser.execute_javascript("window.close()")
        self.data_dict_list = data_dict_list

    def write_data_to_excel(self):
        """
        Writes the data extracted to an excel file
        """

        files.create_workbook(path="{}/cast_crew_data.xlsx".format(OUTPUT_FOLDER))

        for artist_dict in self.data_dict_list:

            for key, value in artist_dict.items():

                artist_name = key
                files.create_worksheet(name=artist_name, content = None, exist_ok = False, header = False)

                excel_dict_list = []

                movies_genres = value

                for elem in movies_genres:
                    excel_dict_list.append({"movie_name": elem[0], "movie_genre": elem[1]})

            files.append_rows_to_worksheet(excel_dict_list, name =artist_name, header=False, start=None)

        files.remove_worksheet(name="Sheet")
        files.save_workbook(path=None)
        files.close_workbook()
