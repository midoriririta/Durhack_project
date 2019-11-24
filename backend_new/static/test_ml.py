#from urllib import urljoin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import pickle

import flask
from flask import Flask, request, url_for, Response
from sklearn.externals import joblib
with open('model_pickle', 'rb') as f:
    mp = pickle.load(f)
print('eg: bread,wine,curry,rice')
test= input(': ')
test= [test]
#self._vectorizer = vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['ing_mod'])

#self._vectorizer = vectorizer
test_= vectorizer.transform(test)

res=mp.predict(test_)
res_map=[]
for i in res:
    res_map.append(cuisine_map[str(i)])
print(res_map)
