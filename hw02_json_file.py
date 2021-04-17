import json

import hw_base

class JSONFile:
    SMARTPHONE_STR = "Smartphone"
    INTERNAL_ID_STR = "iid"
    MEMORY_STR = "Объем встроенной памяти"
    SCREEN_STR = "Разрешение экрана"

    def __init__(self, filename: str):
        self.filename = filename
        self.data = dict()
        with open(filename, 'r', encoding="utf-8") as json_file:
            self.data = json.load(json_file)

    @staticmethod
    def save(filename: str, data: dict):
        with open(filename, 'w', encoding="utf-8") as saved_file:
            json.dump(data, saved_file, indent=4, ensure_ascii=False)

    def characteristics(self, title: str) -> dict:
        return self.data.get(title)

    def get_id(self, title: str) -> int:
        return self.data.get(title).get(self.INTERNAL_ID_STR)

    def get_title_by_id(self, id: int) -> str:
        for title, characteristics in self.data.items():
            if characteristics.get(self.INTERNAL_ID_STR) == id:
                return title
        return "UNKNOWN"

    @staticmethod
    def preparse_smartphones(shopname: str):
        data = dict()
        with open(hw_base.TARGET_DATA_PATH + '/' + shopname + ".json", 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)
        
        result = dict()
        smartphones = data.get("Smartphones")
        for i, smartphone in enumerate(smartphones):
            if not smartphone.get(JSONFile.SMARTPHONE_STR) is None:
                smartphone_name = smartphone.get(JSONFile.SMARTPHONE_STR)
                characteristics = smartphone.get("characteristics")
                characteristics.update({JSONFile.INTERNAL_ID_STR : i})
                result.update({smartphone_name : characteristics })
        JSONFile.save(hw_base.TMP_PATH + '/' + shopname + ".json", result)
        return JSONFile(hw_base.TMP_PATH + '/' + shopname + ".json")
