var querystring = require("querystring"),
fs = require("fs"),
formidable = require("formidable");
var sys = require('sys');

function chart(response) {
    // var index = fs.readFileSync('chart2.html')
    // console.log("Request handler 'chart' was called.");
    // console.log("contecnt index: %s", index)
    // response.writeHead(200, {"Content-Type": "text/html"});
    // response.write(index, "binary");
    // response.end();
    servStatic(response, '/chart2.html')
}

function servStatic(response, pathname) {
    var index = fs.readFileSync("." + pathname)
    console.log("Request handler 'static' was called.: %s", pathname);

    response.writeHead(200, {"Content-Type": "text/html"});
    response.write(index, "binary");
    response.end();    
}

exports.start = start;
exports.upload = upload;
exports.show = show;
exports.chart = chart
exports.servStatic = servStatic
