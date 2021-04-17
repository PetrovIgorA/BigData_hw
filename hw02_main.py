from hw02_json_file import JSONFile
import hw_base
import os

try:
    os.mkdir(hw_base.TMP_PATH)
    os.system("python hw02_record_linkage.py target_data/dns.txt")
    os.remove(hw_base.TMP_PATH)
except OSError as os_error:
    print(os_error)
