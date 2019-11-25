l_file = open("l_file.txt", "r")
    
ingredients = eval(l_file.read()) 

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(ingredients)
    
cuisine_map={'0':'brazilian', '1':'british', '2':'cajun_creole',
'3':'chinese', '4':'filipino', '5':'french', '6':'greek', '7':'indian',
'8':'irish', '9':'italian', '10':'jamaican', '11':'japanese',
'12':'korean', '13':'mexican', '14':'moroccan', '15':'russian',
'16':'southern_us', '17':'spanish', '18':'thai', '19':'vietnamese'}

import joblib

with open('lin_clf.joblib', 'rb') as f:
    mp = joblib.load(f)

test = ['redwine,red curry ','bread']

test_ = vectorizer.transform(test)

res = mp.predict(test_)

for i in res:
    print("suggestion is", cuisine_map[str(i)])


