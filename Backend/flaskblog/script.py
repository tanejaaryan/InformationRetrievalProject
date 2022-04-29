def func( Branches, Interests, Major, Minor, Levels, Courses, Credits):
  
  import pandas as pd
  import numpy as np

  data = pd.read_csv(r"C:\Users\palak\Downloads\InformationRetrievalProject-main (1)\InformationRetrievalProject-main\Backend\flaskblog\Data.csv")

  data.dropna( inplace = True, thresh = 0.5)

  data.replace( np.nan, 0, inplace = True)

  data.reset_index( drop = True, inplace = True)

  data1 = data.copy()

#######################################

  code = data['course_code']
  codes = list(code)
  course_code = [ c.replace(" ","") for c in codes]
  data['course_code'] = course_code

#######################################

  #!pip install contractions
  import contractions

  import nltk
  nltk.download('punkt')
  nltk.download('stopwords')
  nltk.download('wordnet')

  from nltk.tokenize import word_tokenize

  from nltk.stem import WordNetLemmatizer
  lemmatizer = WordNetLemmatizer()

  stopwords = nltk.corpus.stopwords.words('english')


  def remove_stopwords(words):
      words = [i for i in words if i not in stopwords]
      return words

  def remove_punctuation(word):
      punctuation = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
      for ele in word:  
          if ele in punctuation:  
              word = word.replace(ele, "") 
      return word



#############################################

  topic = data['lecture_topic']
  topics = list(topic)
  cnt = 0

  for t in topics:

    words = []
    
    t = t.lower()
    t = contractions.fix(t)

    for word in word_tokenize(t):
      if word and word.strip():
        words.append(word)
    
    words = [i.strip() for i in words]
    
    words = remove_stopwords(words)
    
    words = [remove_punctuation(i) for i in words]
    
    topics[cnt] = words
    cnt += 1


  data['lecture_topic'] = topics

##########################################

  topic = data['mandatory_prereqs']
  topics = list(topic)
  cnt = 0

  for t in topics:

    words = []
    t = str(t)
    t = t.lower()
    t = contractions.fix(t)

    for word in word_tokenize(t):
      if word and word.strip():
        words.append(word)
    
    words = [i.strip() for i in words]
    
    words = remove_stopwords(words)
    
    words = [remove_punctuation(i) for i in words]
    
    topics[cnt] = words
    cnt += 1


  data['mandatory_prereqs'] = topics

###########################################

  topic = data['course_desc']
  topics = list(topic)
  cnt = 0

  for t in topics:

    words = []

    t = t.lower()
    t = contractions.fix(t)

    for word in word_tokenize(t):
      if word and word.strip():
        words.append(word)
    
    words = [i.strip() for i in words]
    
    words = remove_stopwords(words)
    
    words = [remove_punctuation(i) for i in words]
    
    topics[cnt] = words
    cnt += 1


  data['course_desc'] = topics


 ##############################################


  topic = data['course name']
  topics = list(topic)
  cnt = 0

  for t in topics:

    words = []

    t = t.lower()
    t = contractions.fix(t)

    for word in word_tokenize(t):
      if word and word.strip():
        if word.find("xlsx"):
          word = word.replace("xlsx","")
        words.append(word)
    
    words = [i.strip() for i in words]
    
    words = remove_stopwords(words)
    
    words = [remove_punctuation(i) for i in words]

    if words[0] == "visualdesignandcommunication":
      words = ["visual","design","communication"]
    
    topics[cnt] = words
    cnt += 1


  data['course name'] = topics

######################################


  codes = list(data['course_code'])
  c = []
  for code in codes:
    c.append(code[3:])
  data['course_code'] = c

######################################

  def preprocess( s):
    
    s = s.lower()
    s = contractions.fix(s)
    words = []
    for word in word_tokenize(s):
      if word and word.strip():
        words.append(word)
    
    words = [i.strip() for i in words]
    words = remove_stopwords(words)
    words = [remove_punctuation(i) for i in words]

    return words

#######################################

  def focus_retrieve (Focus):

    DATA = pd.DataFrame()
    
    if Focus.find("quizzes")>=0:
      DATA = data[ data.quiz_eval >=15]

    elif Focus.find("assignments")>=0:
      DATA = data[ data.assignment_eval >=20]

    elif Focus.find("projects")>=0:
      DATA = data[ data.project_eval >=20]

    elif Focus.find("exams")>=0:
#       print("exams")
      DATA = data[ data.mid_eval + data.end_eval >=35]

    return DATA


########################################

  def Not_focus_retrieve (Focus):

    DATA = pd.DataFrame()
    
    if Focus.find("quizzes")>=0:
      DATA = data[ data.quiz_eval <=15]

    elif Focus.find("assignments")>=0:
      DATA = data[ data.assignment_eval <=20]

    elif Focus.find("projects")>=0:
      DATA = data[ data.project_eval <=20]

    elif Focus.find("exams")>=0:
      DATA = data[ data.mid_eval + data.end_eval <=35]

    return DATA


####################################

  def similarity( l1, l2):
    intersection = len(set(l1) & set(l2))
    union = len(set(list(l1) + list(l2)))
    coefficient = intersection / union
    return coefficient


####################################

  import collections

  def interest_retrieve( Interests):
    J = {}
    cnt = 0
    course_description = [a+b for a,b in zip( list(data['course_desc']) , list(data['lecture_topic']) ) ]

    for course in course_description:
      J[cnt] = similarity( course, Interests)
      cnt += 1
    J = (sorted(J.items(), key =lambda kv:(kv[1], kv[0]),reverse=True))
    J = collections.OrderedDict(J)
    final = []
    for j in J:
      if len(final) >15:
        break
      final.append(j)
    return data.loc[final]

################################

  def branch_retrieve( Branches):
#     print(Branches)
    DATA = pd.DataFrame()
    
    for Branch in Branches:
      DATA = DATA.append(data[ data.department == Branch])
#       print(DATA)

    return DATA

################################

  def Level_retrieve( Levels):

    DATA = pd.DataFrame()
    
    for Level in Levels:
      DATA = DATA.append(data[ data.level_of_course == Level])

    return DATA

#################################


  def Credits_retreive(Credits):

    DATA = pd.DataFrame()
#     print(Credits)
    for c in Credits:
      DATA = DATA.append( data[ data.course_credits == int(c)])

    return DATA

#################################

  D1 = branch_retrieve( Branches)
#   print(D1)

  Courses = preprocess( Courses)
  D2 = interest_retrieve( Courses)
#   print(D2)
  
  D3 = pd.DataFrame()
  if Major != None:
    Major = Major.lower()
    Major = Major.strip()
    D3 = focus_retrieve( Major)
#     print(D3)
  
  D4 = pd.DataFrame()
  if Minor != None:
    Minor = Minor.lower()
    Minor = Minor.strip()
    D4 = Not_focus_retrieve( Minor)
#     print(D4)
  D5 = pd.DataFrame()
  if len(Interests) > 2:
    Interests = preprocess( Interests)
#   print( Interests)
    D5 = interest_retrieve( Interests)
#   print(D5)

  D6 = Level_retrieve( Levels)
#   print(D6)

  D7 = Credits_retreive(Credits)

  
  l1 = D1.index
  l2 = D2.index
  l3 = D3.index
  l4 = D4.index
  l5 = D5.index
  l6 = D6.index
  l7 = D7.index

  l2 = list(l2)+list(l5)
  
  l = [l1,l2,l3,l4,l6,l7]
  f = []
  for i in l:
    if len(i)!=0:
      f.append(i)

  elements_in_all = list(set.intersection(*map(set, f)))

  D = data1.loc[ elements_in_all]
  D.drop(["lecture_topic", "end_eval", "project_eval", "quiz_eval", "assignment_eval", "mid_eval", "assessment_plan"], axis=1, inplace=True)
    
  return D


def func1( Course_Code):

  import pandas as pd
  import numpy as np

  data = pd.read_csv(r"C:\Users\palak\Downloads\InformationRetrievalProject-main (1)\InformationRetrievalProject-main\Backend\flaskblog\Data.csv")

  data.dropna( inplace = True, thresh = 0.5)

  data.replace( np.nan, 0, inplace = True)

  data.reset_index( drop = True, inplace = True) 

  data1 = data.copy()

  
  code = data['course_code']
  codes = list(code)
  course_code = [ c.replace(" ","") for c in codes]
  data['course_code'] = course_code

  DATA = data[ data.course_code == Course_Code]
  DATA.drop(["lecture_topic", "end_eval", "project_eval", "quiz_eval", "assignment_eval", "mid_eval", "assessment_plan"], axis=1, inplace=True)
  return DATA


def func2( Course_Name):

  import pandas as pd
  import numpy as np

  def cosine_similarity( X, Y):
    X_set = set(X)
    Y_set = set(Y)
    l1 =[];l2 =[]
    rvector = X_set.union(Y_set) 
    for w in rvector:
        if w in X_set: l1.append(1) 
        else: l1.append(0)
        if w in Y_set: l2.append(1)
        else: l2.append(0)
    c = 0
      
    # cosine formula 
    for i in range(len(rvector)):
            c+= l1[i]*l2[i]
    cosine = c / (float((sum(l1)*sum(l2))**0.5) + .0000000001)
    return cosine

  #!pip install contractions
  import contractions

  import nltk
  nltk.download('punkt')
  nltk.download('stopwords')
  nltk.download('wordnet')

  from nltk.tokenize import word_tokenize

  from nltk.stem import WordNetLemmatizer
  lemmatizer = WordNetLemmatizer()

  stopwords = nltk.corpus.stopwords.words('english')


  def remove_stopwords(words):
      words = [i for i in words if i not in stopwords]
      return words

  def remove_punctuation(word):
      punctuation = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
      for ele in word:  
          if ele in punctuation:  
              word = word.replace(ele, "") 
      return word

  
  def preprocess( s):
    
    s = s.lower()
    s = contractions.fix(s)
    words = []
    for word in word_tokenize(s):
      if word and word.strip():
        words.append(word)
    
    words = [i.strip() for i in words]
    words = remove_stopwords(words)
    words = [remove_punctuation(i) for i in words]

    return words

  Course_Name = preprocess(Course_Name)
  # print(Course_Name)


  cos = 0
  pos = 0
  DATA = pd.DataFrame()
  data = pd.read_csv(r"C:\Users\palak\Downloads\InformationRetrievalProject-main (1)\InformationRetrievalProject-main\Backend\flaskblog\Data.csv")

  data.dropna( inplace = True, thresh = 0.5)

  data.replace( np.nan, 0, inplace = True)

  data.reset_index( drop = True, inplace = True) 

  data1 = data.copy()

  
  topic = data['course name']
  topics = list(topic)
  cnt = 0
  pos = 0
  for t in topics:

    words = []

    t = t.lower()
    t = contractions.fix(t)

    for word in word_tokenize(t):
      if word and word.strip():
        if word.find("xlsx"):
          word = word.replace("xlsx","")
        words.append(word)
    
    words = [i.strip() for i in words]
    
    words = remove_stopwords(words)
    
    words = [remove_punctuation(i) for i in words]

    if words[0] == "visualdesignandcommunication":
      words = ["visual","design","communication"]
    
    topics[cnt] = words
    cosine = cosine_similarity(words,Course_Name)
    # pos = cnt
    # print(pos)
    if cosine> cos:
      cos = cosine
      pos = cnt

    cnt += 1


  data['course name'] = topics

  # data.rename({'course name': 'coursename'},axis =1,inplace = True)
  DATA = data1.loc[[pos]]
  DATA.drop(["lecture_topic", "end_eval", "project_eval", "quiz_eval", "assignment_eval", "mid_eval", "assessment_plan"], axis=1, inplace=True)
  
  return DATA
