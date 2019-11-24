var express = require('express');
var app = express();
var axios = require('axios');

var port = 5500;

var response_body = function(http_status, data) {
  return {
    code: http_status.code,
    msg: http_status.msg,
    data: data
  };
};

var result_code = function(code, msg) {
  return {
    code: code,
    msg: msg
  };
};

var h_200 = result_code(200, 'ok');
var h_304 = result_code(304, 'not modified');
var h_400 = result_code(400, 'bad request');
var h_404 = result_code(404, 'not found');
var h_500 = result_code(500, 'internal server error');
var h_502 = result_code(502, 'bad gateway');

app.get('/', (req, res) => {
  res.send('hello world');
});

// post current latitude and longitude
app.get('/location', (req, res) => {
  let location = {
    latitude: req.query.latitude,
    longitude: req.query.longitude
  };
  _res =
    location.latitude && location.longitude
      ? response_body(h_200, location)
      : response_body(h_400, {});
  res.json(_res);
});

// get suggestion
app.get('/suggestions', (req, res) => {
  latitude = req.query.latitude ? req.query.latitude : 54.776100,
  longitude = req.query.longitude ? req.query.longitude : -1.573300,
  favourate = req.query.fav ? req.query.fav : "None"

let suggestion = [];
  
body = count_distance()
console.log(body.data)
let body_list = body.data.results; // an array holds all the restaurant information within the given distance
let opt_result = []; // a summarised key information array
for (let i of body_list) {

    let distance = cal_distance({lat : latitude, lng : longitude}, i.geometry.location)
    obj = {
        place_id : i.place_id,
        location : i.geometry.location,
        name : i.name,
        rating : i.rating,
        vicinity : i.vicinity,
        distance : distance.data.rows.element.distance
    }

    opt_result.push(obj)
}

res.json(opt_result);

});

const count_distance = async () => {
  let url =
  `https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=${latitude},${longitude}&radius=5000&type=restaurant&keyword=cruise&key=AIzaSyDKrDMLj4BDtVjQArzeZl9JBWHTlQYRfJ4`;

  return await axios.get(url) }

const cal_distance = async (o_location, d_location) =>  {
  let url = `https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=${o_location.lat},${o_location.lng}&destinations=${d_location.lat}%2C${d_location.lng}%7C&key=AIzaSyD_wEGTb6Sg6PZCa2tBGD0LkD66apEXWpU`
  return await axios.get(url)
}

function sigmoid(rating,distance,pricelevel) {
  t = rating - (distance/1000)-Math.abs(pricelevel-2.5)
  return 1/(1+Math.pow(Math.E, -t));
}

// post only one dish
app.post('/ilike', (req, res) => {});

app.listen(port, () => {
  console.log(`Server running on port ${port}!`);
});


