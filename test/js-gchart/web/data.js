var fs=require('fs');

global.cpu_info=[];
global.mem_info=[];
global.disk_info=[];
global.net_info=[];

function load_data(filename,cb){
	fs.readFile(filename,'ascii',function(err,data){
		if(err){
			throw err;
		}
		console.log('read finish');
		var lines=data.split("\n");
		//console.log(lines[1]);
		for(var i=1;i<lines.length-1;i++){//skip last line
			if(lines[i]){
				items=lines[i].split("\t");
				//items[0]=new Date(items[0]);
				cpu_info.push(items.slice(0,6));
				time=[items[0]];
				mem_info.push(time.concat(items.slice(6,11)));
				disk_info.push(time.concat(items.slice(11,18)));
				net_info.push(time.concat(items.slice(18)));
			}
		}
		if(cb){
			cb();
		}else{
			console.log(cpu_info);
		}
	});
}

exports.load_data=load_data;

//load_data('20120424.sty');
//load_data('xx');
