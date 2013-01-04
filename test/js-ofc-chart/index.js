var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandlers");
var redis = require("./redis_chart");

var handle = {}
handle["/"] = requestHandlers.chart;
handle["/chart"] = requestHandlers.chart;
handle["/servStatic"] =  requestHandlers.servStatic2;
handle["/redis"] = redis.chart;
server.start(router.route, handle);
