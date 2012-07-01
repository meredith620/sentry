var fs = require("fs");
var path = require("path");

function route(handle, pathname, response, request) {
    console.log("About to route a request for " + pathname);
    if (typeof handle[pathname] === 'function') {
        handle[pathname](response, request);
    }
    else if(pathname.match(".html") ||
           pathname.match(".*")) {
        console.log("static %s", pathname)
        handle["/servStatic"](response, pathname);
    }
    else {
        console.log("No request handler found for " + pathname);
        response.writeHead(404, {"Content-Type": "text/html"});
        response.write("404 Not found");
        response.end();
    }
}

exports.route = route;
