// var data_model = { "elements": [ { "type": "area", "width": 2, "dot-style": { "type": "dot", "colour": "#9C0E57", "dot-size": 3 }, "colour": "#C4B86A", "fill": "#C4B86A", "fill-alpha": 0.7, "on-show": { "type": "pop-up", "cascade": 2, "delay": 0.5 }, "values": [] } ], "title": { "text": "Area Chart" }, "y_axis": { "min": 0, "max": 8, "steps": 2, "labels": ["a", "b", "c", "d", "e"], "offset": 0 }, "x_axis": { "labels": { "steps": 4, "rotate": 270 , "labels": ["a", "b", "c", "d", "e"]}, "steps": 4, "min": 0, "max": 100 } }
var data_model = { "elements": [ { "type": "area", "width": 2, "dot-style": { "type": "dot", "colour": "#9C0E57", "dot-size": 3 }, "colour": "#C4B86A", "fill": "#C4B86A", "fill-alpha": 0.7, "values": [] } ], "title": { "text": "" }, "y_axis": { "min": 0, "max": 100000, "steps": 1, "labels": [], "offset": 0 }, "x_axis": { "labels": { "steps": 4, "rotate": 270 , "labels": []}, "steps": 1, "min": 0, "max": 2880 } }

var key_map = {"time":/\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]3/, "keys": /\[keys=(\d+)\]/, "tps": /\[tps=(\d+)\]}/, "mem": /\[mem=(\d+)\]/}
var data_map = {"time":data_model, "keys": data_model, "tps": data_model, "mem": data_model}
data_map["keys"]["title"]["text"] = "keys"
data_map["tps"]["title"]["text"] = "tps"
data_map["mem"]["title"]["text"] = "mem"

var filename = "redis_log/2012/12/28/all_master_20121228.log"

var fs = require('fs')
var data_ready = false;
function prepare_data() {
    if (data_ready) {
        return;
    }

    function process_line(line) {
        for (k in key_map) {
            var da = key_map[k].exec(line)
            if (da != null) {
                data_map[k]["elements"][0]["values"][data_map[k]["elements"][0]["values"].length] = parseInt(da[1], 10)
            }
        }
    }
    
    // fs.readFile(filename, function(err, data) {    
    //     var res = data.toString().split("\n");
    //     for (i in res) {
    //         process_line(res[i])
    //     }
    //     data_ready = true
    // });
    
    var res = fs.readFileSync(filename).toString().split("\n")
    for (i in res) {
        process_line(res[i])
    }
    data_ready = true
}

// var res = fs.readFileSync(filename).toString().split("\n")
// for (i in res) {
//     process_line(res[i])
// }
// console.log("data ready")
    
function tps_chart_data() {
    prepare_data();
    return JSON.stringify(data_map["tps"]);
    // return data_map["tps"]
}

function keys_chart_data() {
    prepare_data();
    return JSON.stringify(data_map["keys"]);
    // return data_map["keys"]
}

function mem_chart_data() {
    // return JSON.stringify(data_map["mem"]);
    return data_map["mem"]
}

// function read_chart_data(target_date) {    
// }

console.log("log:", keys_chart_data())
