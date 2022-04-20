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
import json

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
# print(xlsx_files)
# print(docx_files)
# exit()
import openpyxl
import string
def getcoursecredits(course_credits, wb_obj, sheet):
    try:
        string1 = chr(ord(course_credits[0]) + 1);
        num1 = int(course_credits[1:])
        string = string1 + str(num1)
        # print(string)
        return int(sheet[string].value)
    except:
        return 4;
def getcoursecode(course_code, wb_obj, sheet):
    string1 = chr(ord(course_code[0]) + 1);
    num1 = int(course_code[1:])
    string = string1 + str(num1)
    # print(string)
    return sheet[string].value

def getcoursedesc(course_desc, wb_obj ,sheet):
    string1 = chr(ord(course_desc[0]) + 1);
    num1 = int(course_desc[1:])
    string = string1 + str(num1)
    # print(string)
    return sheet[string].value

def gettopics(topic, wb_obj, sheet):
    string = ""
    f = True
    list_of_topics = []
    while f:
        string1 = topic[0];
        string2 = int(topic[1:]) + 1; 
        string = string1 + str(string2)
        topic = string
        if (sheet[string].value != None):
            list_of_topics.append(sheet[string].value)
        else:
            f  = False;
    return list_of_topics


def getassessment(assessment_plan, wb_obj, sheet):
    string= ""
    dictionary_assessment = {}
    count = 1; 
    f = True
    while (f):
        string1 = assessment_plan[0];
        string2 = int(assessment_plan[1:]) + count;
        if (sheet[string1 + str(string2)].value!= None):
            strr = chr(ord(course_desc[0]) + 1) + str(string2);
            dictionary_assessment[sheet[string1 + str(string2)].value] = sheet[strr].value
            count += 1; 
        else:
            break;
    return dictionary_assessment; 

def get_mandatory_course_prereqs(course_prereqs, wb_obj, sheet):
    string1 = course_prereqs[0]; 
    string2 = str(1 + int(course_prereqs[1:]))
    if (sheet[string1 + string2].value != None):
        ans = sheet[string1 + string2].value; 
        return ans; 
    return None; 


dictionary_course_name = {}

for i in range(len(xlsx_files)):
    # print(xlsx_files[i])
    # break
    wb_obj = openpyxl.load_workbook(join(PATH, xlsx_files[i]), read_only=True, data_only=True) 
    sheet  = wb_obj.active
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
                actual_course_desc = getcoursedesc(course_desc, wb_obj, sheet)
                # print(actual_course_desc)
            # elif cell_value.lower() == "pre-requisites":
            #     pre_req = cell_address
            elif cell_value.lower() == "lecture topic" or cell_value.lower() == "topics":
                topic = cell_address
                actual_topics = gettopics(topic, wb_obj, sheet)
                # print(actual_topics)
            elif cell_value.lower() == "assessment plan":
                assessment_plan = cell_address
                dictionary_assessment_plan = getassessment(assessment_plan, wb_obj, sheet)
            elif cell_value.lower() == "course code":
                course_code = cell_address
                actual_course_code = getcoursecode(course_code, wb_obj, sheet)
            elif cell_value.lower() == "credits":
                course_credits = cell_address
                actual_course_credits = getcoursecredits(course_credits, wb_obj, sheet)
            elif "pre-requisite" in cell_value.lower() and "mandatory" in cell_value.lower():
                prereqs = cell_address
                mandatory_prereqs = get_mandatory_course_prereqs(prereqs, wb_obj, sheet); 


    try:
        dictionary_xx = {}

        dictionary_xx["course_credits"] = actual_course_credits
        dictionary_xx["course_code"] = actual_course_code
        dictionary_xx["course_desc"] = actual_course_desc
        dictionary_xx["lecture topic"] = actual_topics
        dictionary_xx["assessment plan"] = dictionary_assessment_plan
        # print(dictionary_xx)
        dictionary_xx["level_of_course"] = int(actual_course_code[-3])
        dictionary_xx["mandatory_prereqs"] = mandatory_prereqs
        dictionary_xx["department"] = actual_course_code[:3]
        dictionary_course_name[xlsx_files[i]] = dictionary_xx
        # print(dictionary_xx)
    except Exception as e:
        # print(e)
        print(xlsx_files[i]);
    # if (dictionary_xx["mandatory_prereqs"] != None):
    #     exit()
    # break;
    # break

    # if not course_desc or not topic or not assessment_plan:
    #     print(course_desc, topic, assessment_plan)
    #     print(xlsx_files[i])
print(len(list(dictionary_course_name.keys())))
import json
with open("course_details_updated.json", "w") as outfile:
    json.dump(dictionary_course_name, outfile)
