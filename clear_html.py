import hw_base
from bs4 import BeautifulSoup

class HTMLCleaner:

    def __init__(self, filename : str):
        self.filename = filename
        separated_parts_of_filename = self.filename.split('/')
        self.shopname = separated_parts_of_filename[0]
        self.raw_data_filename = separated_parts_of_filename[1]
        self.title = ""
        self.characteristics = []

    def clear(self):
        if self.shopname == "dns":
            self.__clear_dns()
        elif self.shopname == "citilink":
            self.__clear_citilink()

    def __clear_dns(self):
        TITLE_CLASS = "price_item_description"
        START_TITLE_STR = "Смартфон"
        CHARACTERISTICS_CLASS = "product-characteristics options-group"
        with open(hw_base.RAW_DATA_PATH + '/' + self.filename, "r", encoding="utf-8") as raw_data_file:
            html_str = raw_data_file.read()
        bsoup = BeautifulSoup(html_str, 'html.parser')
        title_text = BeautifulSoup(str(bsoup.find("div", class_=TITLE_CLASS)), 'html.parser').find("h2").text
        self.title = title_text[title_text.find(START_TITLE_STR) + len(START_TITLE_STR) + 1:]
        #hw_base.debug(self.title)
        characteristics_elem = BeautifulSoup(str(bsoup.find("div", class_=CHARACTERISTICS_CLASS)), 'html.parser').find("table")
        table_elem = BeautifulSoup(str(characteristics_elem), 'html.parser').find_all("tr")
        for tr in table_elem:
            td_elems = BeautifulSoup(str(tr), 'html.parser').find_all("td")
            if (len(td_elems) == 2):
                char_name = BeautifulSoup(str(td_elems[0]), 'html.parser').find("span").text.strip().replace('\n', '')
                val_name = BeautifulSoup(str(td_elems[1]), 'html.parser').find("div").text.strip().replace('\n', '')
                #hw_base.debug(char_name, val_name)
                self.characteristics.append((char_name, val_name))
                

    def __clear_citilink(self):
        CHARACTERISTICS_CLASS = "Specifications__row"
        TITLE_CLASS = "Heading Heading_level_1 ProductHeader__title"
        START_TITLE_STR = "смартфон"
        CHAR_NAME_STR = "Specifications__column Specifications__column_name"
        CHAR_VALUE_STR = "Specifications__column Specifications__column_value"
        with open(hw_base.RAW_DATA_PATH + '/' + self.filename, "r", encoding="utf-8") as raw_data_file:
            html_str = raw_data_file.read()
            title_text = BeautifulSoup(html_str, 'html.parser').find("h1", class_=TITLE_CLASS).text.strip()
            end_of_title = title_text.find('\n')
            if end_of_title == -1:
                end_of_title = len(title_text)
            self.title = title_text[title_text.find(START_TITLE_STR) + len(START_TITLE_STR) + 1:end_of_title]
            #hw_base.debug(self.title)
            characteristics_elem = BeautifulSoup(html_str, 'html.parser').find_all("div", class_=CHARACTERISTICS_CLASS)
            for row in characteristics_elem:
                char_name = BeautifulSoup(str(row), 'html.parser').find("div", class_=CHAR_NAME_STR).text.strip()
                end_of_char_name = char_name.find('\n')
                if end_of_char_name == -1:
                    end_of_char_name = len(char_name)
                char_name = char_name[:end_of_char_name]
                val_name = BeautifulSoup(str(row), 'html.parser').find("div", class_=CHAR_VALUE_STR).text.strip().replace('\n', '')
                #hw_base.debug(char_name, val_name)
                self.characteristics.append((char_name, val_name))
            

if __name__ == "__main__":
    with open(hw_base.WORKSPACE_PATH + "/list_of_citilink_data.txt", "r") as file:
        for line in file.readlines():
            if line[0] == '#':
                continue
            cleaner = HTMLCleaner(line)
            cleaner.clear()
