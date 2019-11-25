from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import requests
from urllib.request import urlretrieve

def find_cuisine(ipt):
    base_url = "http://localhost:5000/static/%s"
    urlretrieve(base_url % "l_file.txt", "./static/l_file.txt")
    urlretrieve(base_url % "lin_clf.joblib", "./static/lin_clf.joblib")

    with open("l_file.txt", "r") as f:
        ingredients = eval(f.read())

    with open("lin_clf.joblib", "rb") as f:
        mp = joblib.load(f)

    cuisine_map = ['brazilian', 'british', 'cajun_creole', 'chinese', 'filipino', 'french', 'greek', 'indian', 'irish', 'italian', 'jamaican', 'japanese', 'korean', 'mexican', 'moroccan', 'russian', 'southern_us', 'spanish', 'thai', 'vietnamese']

    vectorizer = TfidfVectorizer()

    X = vectorizer.fit_transform(ingredients)

    test = [ipt]

    test = vectorizer.transform(test)

    res = mp.predict(test)

    res_str = []

    for i in res:
        res_str.append(cuisine_map[i])

    return res_str

if __name__ == "__main__":
    print(find_cuisine(input("input: ")))