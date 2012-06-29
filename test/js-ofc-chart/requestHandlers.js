var querystring = require("querystring"),
fs = require("fs");
// formidable = require("formidable");
var sys = require('util');

function chart(response) {
    // var index = fs.readFileSync('chart2.html')
    // console.log("Request handler 'chart' was called.");
    // console.log("contecnt index: %s", index)
    // response.writeHead(200, {"Content-Type": "text/html"});
    // response.write(index, "binary");
    // response.end();
    servStatic(response, '/chart.html')
}

function servStatic(response, pathname) {
    var index = fs.readFileSync("." + pathname)
    console.log("Request for %s", pathname);

    response.writeHead(200, {"Content-Type": "text/html"});
    response.write(index, "binary");
    response.end();    
}

exports.chart = chart
exports.servStatic = servStatic
