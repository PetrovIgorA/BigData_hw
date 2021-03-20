from mrjob.job import MRJob
import hw_base
from clear_html import HTMLCleaner
import sys

shopname = ""
count_files = 0

class MRHTML2JSON(MRJob):

    def init(self):
        self.shopname = shopname
        with open(hw_base.CONVERTED_DATA_PATH + "/" + shopname + ".json", "a", encoding="utf-8") as json_file:
            json_file.write("{\n")
            json_file.write("\t\"shop\": " + "\"" + shopname + "\",\n")
            json_file.write("\t\"Smartphones\": [\n")
    
    def cancel(self):
        with open(hw_base.CONVERTED_DATA_PATH + "/" + shopname + ".json", "a", encoding="utf-8") as json_file:
            json_file.write("\t{\n\t\t\"Smartphones count\": " + "\"" + str(count_files) + "\"\n\t}\n")
            json_file.write("]\n")
            json_file.write("}\n")
    
    def mapper(self, _, filename):
        cleaner = HTMLCleaner(filename)
        cleaner.clear()
        self.shopname = cleaner.shopname
        characteristics = cleaner.characteristics
        for characteristic in characteristics:
            yield cleaner.title, characteristic
    
    def reducer(self, key, values):
        values = list(values)
        with open(hw_base.CONVERTED_DATA_PATH + "/" + shopname + ".json", "a", encoding="utf-8") as json_file:
            json_file.write("\t\t{\n")
            json_file.write("\t\t\"Smartphone\": \"" + key + "\",\n")
            json_file.write("\t\t\"characteristics\": {\n")
            char_count = len(values)
            for i in range(0, char_count - 1):
                json_file.write("\t\t\t\"" + values[i][0].replace('\"', '') + "\": \"" + values[i][1].replace('\"', '') +"\",\n")
            json_file.write("\t\t\t\"" + values[char_count - 1][0].replace('\"', '') + "\": \"" + values[char_count - 1][1].replace('\"', '') +"\"\n")
            json_file.write("\t\t}\n\t},\n")



with open(sys.argv[1], "r") as input_file:
    lines = input_file.readlines()
    count_files = len(lines)
    shopname = lines[0].split('/')[0]

runner = MRHTML2JSON()
runner.init()
runner.run()
runner.cancel()
