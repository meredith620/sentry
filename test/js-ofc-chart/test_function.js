console.log("hello")
var text = "[2012-12-28 23:55:07] [keys=14947667] [exps=0] [tps=165300] [mem=7121529360]";
// text = "First line \n second line";
// text = "[2012-12-28 23:55:07] lalala"

var regex_time = /\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]3/;
var match_time = regex_time.exec(text);
var regex_keys = /\[keys=(\d+)\]/;
var match_keys = regex_keys.exec(text);
var regex_tps = /\[tps=(\d+)\]/;
var match_tps = regex_tps.exec(text);
var regex_mem = /\[mem=(\d+)\]/;
var match_mem = regex_mem.exec(text);

function pmatch(match, key) {
    // console.log("NOT match %s", match === null);
    if (match != null) {
        // console.log("0: ", match[0]);
        console.log(key, ":", match[1]);
        // console.log("2: ", match[2]);
        // console.log("3: ", match[3]);
    }
}

console.log("text", ":", text)
pmatch(match_time, "time")
pmatch(match_keys, "keys")
pmatch(match_tps, "tps")
pmatch(match_mem, "mem")

var fs = require('fs')
fs.readFile("data.json", function(err, data) {
    var res = data.toString().split("\n");
    console.log("length: %d", res.length)    
});
// var res = fs.readFileSync("redis.data").toString().split("\n");
// console.log("length: %d", res.length);

// var now = new Date();
// console.log(now.getTime())

// =====  main =====

var data_model = { "elements": [ { "type": "area", "width": 2, "dot-style": { "type": "dot", "colour": "#9C0E57", "dot-size": 7 }, "colour": "#C4B86A", "fill": "#C4B86A", "fill-alpha": 0.7, "on-show": { "type": "pop-up", "cascade": 2, "delay": 0.5 }, "values": [] } ], "title": { "text": "Area Chart" }, "y_axis": { "min": -2, "max": 2, "steps": 2, "labels": null, "offset": 0 }, "x_axis": { "labels": { "steps": 4, "rotate": 270 }, "steps": 2 } }

// var d = {"a":[1,2,3,4,5], "b":[6,7,8,9]}
// console.log("len: ", d["a"].length)
// console.log("?:", "a" in d)

// var regex_time = /\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]3/;
// var regex_keys = /\[keys=(\d+)\]/;
// var regex_tps = /\[tps=(\d+)\]/;
// var regex_mem = /\[mem=(\d+)\]/;

// var regex
// key_map = {}
// regex = /\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]3/;
// key_map["time"] = regex
// regex = /\[keys=(\d+)\]/
// key_map["keys"] = regex
// regex = /\[tps=(\d+)\]/;
// key_map["tps"] = regex
// regex = /\[mem=(\d+)\]/;
// key_map["mem"] = regex
key_map = {"time":/\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]3/, "keys": /\[keys=(\d+)\]/, "tps": /\[tps=(\d+)\]}/, "mem": /\[mem=(\d+)\]/}
data_map = {"time":data_model, "keys": data_model, "tps": data_model, "mem": data_model}
function process_line(line) {
    console.log("line:", line)
    for (k in key_map) {
        // console.log(k,":",key_map[k])
        var da = key_map[k].exec(line)
        if (da != null) {
            data_map[k]["elements"][0]["values"][data_map[k]["elements"][0]["values"].length] = da[1]
            // console.log("k:", k, "da:", da[1])
            console.log("k:", k, data_map[k]["elements"][0]["values"].length)
            }
        }
}

filename = "redis_log/2012/12/28/all_master_20121228.log"
fs.readFile(filename, function(err, data) {
    var res = data.toString().split("\n");
    for (i in res) {
        process_line(res[i])
    }
    // for (x in data_map) {
    //     console.log(x, ":", data_map[x]["elements"][0]["values"].length)
    //     // console.log(x, ":", JSON.stringify(data_map[x]));
    // };
});
