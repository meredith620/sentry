console.log("hello")
var text = "[2012-12-14 18:56:09.466] 123 324";
text = "First line \n second line";

var regex = /[(\S+ \S+)] .*/;
var match = regex.exec(text);
console.log("NOT match %s", match === null);
console.log(match[1]);
console.log(match[2]);
console.log(match[3]);

var fs = require('fs')
// fs.readFile("data.json", function(err, data) {
//     var res = data.toString().split("\n");
//     console.log("length: %d", res.length)    
// });
var res = fs.readFileSync("redis.data").toString().split("\n");
console.log("length: %d", res.length);

// var now = new Date();
// console.log(now.getTime())


