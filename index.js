var express = require('express')
var app = express()
var axios = require("axios")
app.all('*', function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    res.header("Access-Control-Allow-Methods","PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By",' 3.2.1')
    res.header("Content-Type", "application/json;charset=utf-8");
    next();
});
app.get('/',function(req,res){
  var url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=54.776100,-1.573300&radius=1500&type=restaurant&keyword=cruise&key=AIzaSyDKrDMLj4BDtVjQArzeZl9JBWHTlQYRfJ4"
  axios.get(url).then(a => {

    var b =a.data.results
    var len = b.length
    var suggestion = []

    for (var i=0;i<len;i++){
      var result = []
      result.push(b[i].place_id)
      result.push(b[i].geometry.location)
      result.push(b[i].name)
      result.push(b[i].rating)
      result.push(b[i].vicinity)
      suggestion.push(result)
    }
    console.log(suggestion)

  })

})
app.listen(8080,function(){
  console.log('App Listening on port 8080')
})
