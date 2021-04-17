from mrjob.job import MRJob
from mrjob.job import MRStep
import hw_base
from hw01_my_regexp import myregexp
from hw01_clear_html import HTMLCleaner
import sys

shopname = ""
count_files = 0

class MRHTML2JSON(MRJob):

    def init(self):
        self.shopname = shopname
        self.dump_init_json(hw_base.CONVERTED_DATA_PATH + '/' + self.shopname + '.json')
        self.dump_init_json(hw_base.TARGET_DATA_PATH + "/" + shopname + ".json")
    
    def cancel(self):
        self.dump_cancel_json(hw_base.CONVERTED_DATA_PATH + '/' + self.shopname + '.json')
        self.dump_cancel_json(hw_base.TARGET_DATA_PATH + "/" + shopname + ".json")

    @staticmethod
    def make_target_characteristic(characteristic : tuple):
        with open(hw_base.TARGET_CHARACTERISTICS_PATH, "r", encoding="utf-8") as rules_file:
            res = hw_base.UNUSED_CHARACTERISTICS_NAME
            for rule in rules_file.readlines():
                index = rule.find('->')
                res = myregexp(characteristic[0], rule[:index - 1], rule[index + 3:-1])
                if res != hw_base.UNUSED_CHARACTERISTICS_NAME:
                    break
            characteristic[0] = res
        return characteristic

    @staticmethod
    def is_target_characteristic(characteristic: tuple):
        return characteristic[0] != hw_base.UNUSED_CHARACTERISTICS_NAME
    
    def conver_mapper(self, _, filename):
        cleaner = HTMLCleaner(filename)
        cleaner.clear()
        characteristics = cleaner.characteristics
        for characteristic in characteristics:
            yield cleaner.title, characteristic
    
    def convert_reducer(self, key, values):
        values = list(values)
        self.dump_part_json(key, values, hw_base.CONVERTED_DATA_PATH + "/" + shopname + ".json")
        yield key, values

    def target_reducer(self, key, values):
        values = list(values)
        self.dump_part_json(key, values[0], hw_base.TARGET_DATA_PATH + "/" + shopname + ".json",
                            MRHTML2JSON.make_target_characteristic,
                            MRHTML2JSON.is_target_characteristic
                        )
        with open(hw_base.TARGET_DATA_PATH + "/" + shopname + ".txt", "a", encoding="utf-8") as keys_list_file:
            keys_list_file.write(key + '\n')

    def steps(self):
        return [
            MRStep(mapper=self.conver_mapper, reducer=self.convert_reducer),
            MRStep(reducer=self.target_reducer)
        ]

    def dump_init_json(self, filename : str):
        with open(filename, "a", encoding="utf-8") as json_file:
            json_file.write("{\n")
            json_file.write("\t\"shop\": " + "\"" + shopname + "\",\n")
            json_file.write("\t\"Smartphones\": [\n")
    
    def dump_cancel_json(self, filename : str):
        with open(filename, "a", encoding="utf-8") as json_file:
            json_file.write("\t{\n\t\t\"Smartphones count\": " + "\"" + str(count_files) + "\"\n\t}\n")
            json_file.write("]\n")
            json_file.write("}\n")
    
    def dump_part_json(self, title : str, characteristics : list, filename : str,
                       make_target_char = lambda x: x,
                       is_target_char = lambda x: True):
        with open(filename, "a", encoding="utf-8") as json_file:
            json_file.write("\t\t{\n")
            json_file.write("\t\t\"Smartphone\": \"" + title + "\",\n")
            json_file.write("\t\t\"characteristics\": {")
            char_count = len(characteristics)
            is_first = True
            for i in range(0, char_count - 1):
                char = make_target_char(characteristics[i])
                if is_target_char(char):
                    if is_first:
                        json_file.write("\n\t\t\t\"" + char[0] + "\": \"" + char[1] +"\"")
                        is_first = False
                    else:
                        json_file.write(",\n\t\t\t\"" + char[0] + "\": \"" + char[1] +"\"")
            char = make_target_char(characteristics[char_count - 1])
            if is_target_char(char):
                json_file.write(",\n\t\t\t\"" + char[0] + "\": \"" + char[1] +"\"\n")
            json_file.write("\t\t}\n\t},\n")

with open(sys.argv[1], "r") as input_file:
    lines = input_file.readlines()
    count_files = len(lines)
    shopname = lines[0].split('/')[0]

runner = MRHTML2JSON()
runner.init()
runner.run()
runner.cancel()
