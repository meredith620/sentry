var querystring = require("querystring"),
fs = require("fs");
path = require("path");
var sys = require('util');

function chart(response) {
    // var index = fs.readFileSync('chart2.html')
    // console.log("Request handler 'chart' was called.");
    // console.log("contecnt index: %s", index)
    // response.writeHead(200, {"Content-Type": "text/html"});
    // response.write(index, "binary");
    // response.end();
    servStatic2(response, '/chart2.html')
}

function servStatic(response, pathname) {
    var realpath = "." + pathname;
    var index = fs.readFileSync(realpath);

    response.writeHead(200, {"Content-Type": "text/html"});
    response.write(index, "binary");
    response.end();    
}

function servStatic2(response, pathname) {
    var realpath = "." + pathname;
    path.exists (realpath, function (exists){
        if (!exists) {
            response.writeHead(404, {'Content-Type': 'text/plain'});
            response.write("This request URL " + pathname + " was not found on this server.");
            response.end();
        } else {
            fs.readFile(realpath, "binary", function (err, file){
                if(err) {
                    response.writeHead(500, {'Content-Type': 'text/plain'});
                    response.end(err);
                } else {
                    response.writeHead(200, {'Content-Type': 'text/html'});
                    response.write(file, "binary");
                    response.end();
                }
            });
        }
    });
}

exports.chart = chart
exports.servStatic = servStatic
exports.servStatic2 = servStatic2
