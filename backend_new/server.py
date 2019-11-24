from flask import Flask, request, jsonify
from flask_cors import *

import requests
import json
import math

app = Flask(__name__)
CORS(app, supports_credentials=True)
all_resta_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%.4f,%.4f&radius=%.4f&type=restaurant&keyword=%s&key=AIzaSyDKrDMLj4BDtVjQArzeZl9JBWHTlQYRfJ4"
cal_dis_url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=%.4f,%.4f&destinations=%.4f,%.4f&key=AIzaSyD_wEGTb6Sg6PZCa2tBGD0LkD66apEXWpU"



@app.route('/suggestions')
def suggestions():
    lat = float(request.args.get('lat'))
    lng = float(request.args.get('lng'))
    perf = request.args.get('perf')
    mate = request.args.get('mate')
    keyword = "cruise"

    if perf != "" or perf != "undefined":
        keyword = perf
    elif mate != "":
        keyword = mate

    rad = 5000

    print(mate)

    if mate != "a":
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        from nltk.stem import PorterStemmer
        from nltk.tokenize import sent_tokenize, word_tokenize
        import re

        ps = PorterStemmer()
        
        file_ = requests.get("http://localhost:5000/static/train.json").text

        dict_train = json.loads(file_)[:20000]
        #print(dict_train[0])

        id_ = []
        cuisine = []
        ingredients = []
        for i in range(len(dict_train)):
            id_.append(dict_train[i]['id'])
            cuisine.append(dict_train[i]['cuisine'])
            ingredients.append(dict_train[i]['ingredients'])

        import pandas as pd
        df = pd.DataFrame({'id':id_, 
                        'cuisine':cuisine, 
                        'ingredients':ingredients})
        #print(df.head(5))
        df['cuisine'].value_counts()
        #print(df['cuisine'].value_counts())

        new = []
        for s in df['ingredients']:
            s = ' '.join(s)
            new.append(s)
        df['ing'] = new

        #print(new[0])
        import re
        l=[]
        for s in df['ing']:
            
            #Remove punctuations
            s=re.sub(r'[^\w\s]','',s)
            
            #Remove Digits
            s=re.sub(r"(\d)", "", s)
            
            #Remove content inside paranthesis
            s=re.sub(r'\([^)]*\)', '', s)
            
            #Remove Brand Name
            s=re.sub(u'\w*\u2122', '', s) 
            
            #Convert to lowercase
            s=s.lower()
            
            #Remove Stop Words
            stop_words = set(stopwords.words('english'))
            word_tokens = word_tokenize(s)
            filtered_sentence = [w for w in word_tokens if not w in stop_words]
            filtered_sentence = []
            for w in word_tokens:
                if w not in stop_words:
                    filtered_sentence.append(w)
            s=' '.join(filtered_sentence)
            
            #Remove low-content adjectives
            
            
            #Porter Stemmer Algorithm
            words = word_tokenize(s)
            word_ps=[]
            for w in words:
                word_ps.append(ps.stem(w))
            s=' '.join(word_ps)
            
            l.append(s)
        df['ing_mod']=l
        #print(df.head(10))

        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df['ing_mod'])

        #print(X)
        s='1 1cool co1l coo1'
        s=re.sub(r"(\d)", "", s)
        #print(s)

        from nltk.stem import PorterStemmer
        from nltk.tokenize import sent_tokenize, word_tokenize

        ps = PorterStemmer()

        from sklearn import preprocessing
        le = preprocessing.LabelEncoder()
        le.fit(df['cuisine'])
        df['cuisine']=le.transform(df['cuisine'])
        df['cuisine'].value_counts()
        #print(df['cuisine'].value_counts())
        cuisine_map={'0':'brazilian', '1':'british', '2':'cajun_creole',
        '3':'chinese', '4':'filipino', '5':'french', '6':'greek', '7':'indian',
        '8':'irish', '9':'italian', '10':'jamaican', '11':'japanese',
        '12':'korean', '13':'mexican', '14':'moroccan', '15':'russian',
        '16':'southern_us', '17':'spanish', '18':'thai', '19':'vietnamese'}

        Y=[]
        Y = df['cuisine']
        import numpy as np
        from sklearn.preprocessing import Imputer
        #from sklearn.cross_validation import train_test_split
        from sklearn.model_selection import train_test_split
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.metrics import accuracy_score

        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size =
        0.2, random_state = 100)

        from sklearn import svm
        lin_clf = svm.LinearSVC(C=1)
        lin_clf.fit(X_train, y_train)
        y_pred=lin_clf.predict(X_test)
        #print(accuracy_score(y_test,y_pred)*100)
        #print(lin_clf.predict(X_test[0]))
        #print(X_test[0])

        #// 引入包
        import pickle
        from sklearn.svm import LinearSVC

        #// 将模型写入 model_pickle 文件
        with open('model_pickle', 'wb') as f:
            pickle.dump(lin_clf, f)

        #// 从 model_pickle 文件中读取模型
        with open('model_pickle', 'rb') as f:
            mp = pickle.load(f)

        test = [mate]
        test_ = vectorizer.transform(test)

        #// 用模型进行预测
        res = mp.predict(test_)
        res_map = []
        for i in res:
            res_map.append(cuisine_map[str(i)])

        print(res_map)

        if res_map != None and len(res_map) != 0:
            keyword = res_map

    print("now keyword is", keyword)
    all_resta = requests.get(all_resta_url % (lat, lng, rad, keyword)).text
    all_resta_obj = json.loads(all_resta)
    opt_result = []

    print(all_resta_obj)

    for i in all_resta_obj["results"]:
        d_lat = i["geometry"]["location"]["lat"]
        d_lng = i["geometry"]["location"]["lng"]
        dis_obj = json.loads(requests.get(cal_dis_url % (lat, lng, d_lat, d_lng)).text)
        distance = dis_obj["rows"][0]["elements"][0]["distance"]["value"]

        price_level = 0
        try:
            price_level = i["price_level"]
        except:
            pass


        def sigmoid(rating, distance, price_level):
            t = rating - (distance/1000) - math.fabs(price_level-2.5)
            return 1 / (1 + math.pow(math.e, -t))

        def cmp(x):
            return -x["overall_score"]

        i["dis_obj"] = dis_obj
        i["distance"] = distance
        i["overall_score"] = sigmoid(i["rating"], distance, price_level)

        opt_result.append(i)

    opt_result = sorted(opt_result, key=cmp)
    print(opt_result)

    return jsonify(opt_result[:3])

if __name__ == '__main__':
    app.run()
