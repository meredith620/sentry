var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandlers");

var handle = {}
handle["/chart"] = requestHandlers.chart;
handle["/servStatic"] =  requestHandlers.servStatic;

server.start(router.route, handle);
