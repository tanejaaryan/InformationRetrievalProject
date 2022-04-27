import json

f = open("course_details.json")
data = json.load(f)
print(data.keys())
print(len(list(data.keys())))