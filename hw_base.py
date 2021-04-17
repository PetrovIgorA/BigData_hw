import os

WORKSPACE_PATH = os.path.dirname(__file__)
RAW_DATA_PATH = WORKSPACE_PATH + "/raw_data"
CONVERTED_DATA_PATH = WORKSPACE_PATH + "/converted_data"
TARGET_CHARACTERISTICS_PATH = WORKSPACE_PATH + "/hw01_target_characteristics.txt"
TARGET_DATA_PATH = WORKSPACE_PATH + "/target_data"
DEBUG_FILE_PATH = WORKSPACE_PATH + "/debug/debug.txt"

UNUSED_CHARACTERISTICS_NAME = "Unused"

def debug(*args, sep=' ', end='\n', filename=DEBUG_FILE_PATH):
    with open(filename, "a", encoding="utf-8") as file:
        for arg in args:
            file.write(str(arg) + sep)
        file.write(end)

