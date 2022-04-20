import json
import csv
 
# Opening JSON file
with open('course_details_updated.json') as json_file:
    data = json.load(json_file)

data_file = open('final_data_part3.csv', 'w', encoding = 'utf-8')

def process_assessment_plan_mid(assessment):
	keys = list(assessment.keys())
	for num in keys:
		if ("mid" in num.lower()):
			return (assessment[num])
	return None;

def process_assessment_plan_end(assessment):
	keys = list(assessment.keys())
	for num in keys:
		if ("end" in num.lower()):
			return (assessment[num])
	return None;

def process_assessment_plan_project(assessment):
	keys = list(assessment.keys())
	for num in keys:
		if ("project" in num.lower()):
			return (assessment[num])
	return None;

def process_assessment_plan_quizzes(assessment):
	keys = list(assessment.keys())
	for num in keys:
		if ("quiz" in num.lower()):
			return (assessment[num])
	return None;
def process_assessment_plan_assignment(assessment):
	keys = list(assessment.keys())
	for num in keys:
		if ("assignment" in num.lower()):
			return (assessment[num])
	return None;
def process_assessment_plan_homework(assessment):
	keys = list(assessment.keys())
	for num in keys:
		if ("homework" in num.lower()):
			return (assessment[num])
	return None;
# create the csv writer object
csv_writer = csv.writer(data_file)

list_of_keys = list(data.keys());

course_credits = []
course_code = []
course_desc = []
lecture_topic = []
assessment_plan = []
level_of_course = []
mandatory_prereqs = []
department = []
course_name = []
mid_eval =[]
end_eval = []
project_eval = []
quiz_eval = []
course_name = []
assignment_eval = []
homework_eval = []

print(len(list_of_keys))
for key in list_of_keys:
	dictionary_xx = data[key]; 
	course_credits.append(dictionary_xx["course_credits"]) 
	course_name.append(key); 
	course_code.append(dictionary_xx["course_code"])
	course_desc.append(dictionary_xx["course_desc"])
	lecture_topic.append(dictionary_xx["lecture topic"])
	assessment_plan.append(dictionary_xx["assessment plan"])
	level_of_course.append(dictionary_xx["level_of_course"])
	mandatory_prereqs.append(dictionary_xx["mandatory_prereqs"])
	department.append(dictionary_xx["department"])
	# course_name.append(key);
	mid_eval.append(process_assessment_plan_mid(dictionary_xx["assessment plan"]))
	end_eval.append(process_assessment_plan_end(dictionary_xx["assessment plan"]))
	project_eval.append(process_assessment_plan_project(dictionary_xx["assessment plan"]))
	quiz_eval.append(process_assessment_plan_quizzes(dictionary_xx["assessment plan"]))
	assignment_eval.append(process_assessment_plan_assignment(dictionary_xx["assessment plan"]))

	homework_eval.append(process_assessment_plan_homework(dictionary_xx["assessment plan"]))
csv_writer.writerow(["course name", "course_credits", "course_code" , "course_desc" , "lecture_topic" , "assessment_plan", "level_of_course", "mandatory_prereqs", "department",  "mid_eval", "end_eval", "project_eval", "quiz_eval","assignment_eval", "homework_eval"])
r  = 0; 
print(len(course_name))
for i in range(len(list_of_keys)):
  csv_writer.writerow([course_name[i], course_credits[i], course_code[i] ,course_desc[i], lecture_topic[i], assessment_plan[i], level_of_course[i], mandatory_prereqs[i], department[i],  mid_eval[i], end_eval[i], project_eval[i], quiz_eval[i], assignment_eval[i], homework_eval[i]])
  r += 1; 
print(r)

data_file.close()