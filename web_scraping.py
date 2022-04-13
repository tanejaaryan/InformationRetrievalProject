import requests

# URL = "http://techtree.iiitd.edu.in/static/Courses.json?_=1647309709068"
# page = requests.get(URL)

# json_data = page.json()
# print(json_data["data"][0])

# URL2 = "http://techtree.iiitd.edu.in/viewDescription/filename?=BIO101"
# page2 = requests.get(URL2)

# print(page2.text)

PATH = './course_data/'

from os import listdir, remove
from os.path import isfile, join
import pandas as pd

xlsx_files = []
docx_files = []

for file_ in listdir(PATH):
    extension = file_.split('.')[-1]
    if extension == "xlsx":
    # if extension == "xlsx":
        xlsx_files.append(file_)
    elif extension == "docx" or extension == "doc":
        docx_files.append(file_)
    # else:
    #     remove(join(PATH, file_))   # remove pdfs


import openpyxl
import string

for i in range(len(xlsx_files)):
    print(xlsx_files[i])
    wb_obj = openpyxl.load_workbook(join(PATH, xlsx_files[i]), read_only=True, data_only=True) 

    course_desc = ""
    # pre_req = ""
    topic = ""
    assessment_plan = ""

    for cell_num in range(1, 40):
        for cell_name in list(string.ascii_uppercase)[:2]:

            cell_address = cell_name + str(cell_num)
            cell_value = str(wb_obj.active[cell_address].value).strip()
            if not cell_value:
                continue

            if cell_value.lower() == "course description":
                course_desc = cell_address
            # elif cell_value.lower() == "pre-requisites":
            #     pre_req = cell_address
            elif cell_value.lower() == "lecture topic" or cell_value.lower() == "topics":
                topic = cell_address
            elif cell_value.lower() == "assessment plan":
                assessment_plan = cell_address

    # if not course_desc or not topic or not assessment_plan:
    #     print(course_desc, topic, assessment_plan)
    #     print(xlsx_files[i])
