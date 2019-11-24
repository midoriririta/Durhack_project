from flask import Flask, request, jsonify
import requests
import json
import math

app = Flask(__name__)
all_resta_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%.4f,%.4f&radius=%.4f&type=restaurant&keyword=%s&key=AIzaSyDKrDMLj4BDtVjQArzeZl9JBWHTlQYRfJ4"
cal_dis_url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=%.4f,%.4f&destinations=%.4f,%.4f&key=AIzaSyD_wEGTb6Sg6PZCa2tBGD0LkD66apEXWpU"



@app.route('/suggestions')
def suggestions():
    lat = float(request.args.get('lat'))
    lng = float(request.args.get('lng'))
    perf = request.args.get('perf')
    mate = request.args.get('mate')
    keyword = "cruise"

    if perf != "":
        keyword = perf
    elif mate != "":
        keyword = mate

    rad = 5000

    print(keyword)

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
