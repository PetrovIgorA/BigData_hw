## HW, course "Information Extraction and Integration from Big Data"

#### Run all homeworks
```
python hw_main.py
```

### HW 0

We have 2 dataset:

1. html-files with smartphone characteristics from DNS shop
2. html-files with smartphone characteristics from Citilink shop

All raw html-files in `raw_data`

### HW 1

Here is converted raw data to target schema (html -> json). I use 2 MRjob steps (`hw01_html_to_json.py`):

1. Clear raw data (delete useless info, extract usefull parameters), use preparsing in `hw01_clear_html.py`, save in `converted_data`
2. Make json files in alone schema (now we have same attribute names), use my small regular expression in `hw01_my_regexp.py`, save in `target_data`

#### Run
```
python hw01_main_convert.py
```

### HW 2

Entity resolution: record linkage

Here, data from different sources is linked (via MapReduce) using a unique identifier. The input data is located in `target_data` folder. The output data is located in `er_data` folder.

#### Run
```
python hw02_main.py
```

### HW 3

Data fusion

The input data is located in `er_data` folder. Here, data linked by a common attribute is fused into one file `fusion_data/fusion.json` via `fuse_by` function. Data without link with other source is added in result file.

#### Run
```
python hw03_main.py
```