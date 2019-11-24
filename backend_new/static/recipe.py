def run_ml(word_arr):
    import json
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer
    from nltk.tokenize import sent_tokenize, word_tokenize
    import re

    ps = PorterStemmer()
    file = r'../backend_new/train.json'
    with open(file) as train_file:
        dict_train = json.load(train_file)

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

    test = word_arr
    test_ = vectorizer.transform(test)

    #// 用模型进行预测
    res = mp.predict(test_)
    res_map = []
    for i in res:
        res_map.append(cuisine_map[str(i)])
    print(res_map)


if __name__ == "__main__":
    run_ml()
