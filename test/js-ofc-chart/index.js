var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandlers");

var handle = {}
handle["/"] = requestHandlers.chart;
handle["/chart"] = requestHandlers.chart;
handle["/servStatic"] =  requestHandlers.servStatic2;

server.start(router.route, handle);
