from hw02_json_file import JSONFile
import hw_base
import os

try:
    os.mkdir(hw_base.TMP_PATH)
    os.system("python hw02_record_linkage.py target_data/dns.txt")

    dns_json = JSONFile(hw_base.ER_DATA_PATH + "/dns.json")
    citilink_json = JSONFile(hw_base.ER_DATA_PATH + "/citilink.json")

    unique_id_set = set()
    for uid in dns_json.data.keys():
        unique_id_set.add(uid)
    for uid in citilink_json.data.keys():
        unique_id_set.add(uid)
    
    with open(hw_base.UID_PATH, "w", encoding="utf-8") as uid_file:
        for uid in unique_id_set:
            uid_file.write(uid + '\n')

    os.remove(hw_base.TMP_PATH)
except OSError as os_error:
    print(os_error)
