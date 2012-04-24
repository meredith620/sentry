var fs=require('fs');

var cpu_info=[];

function load_data(filename){
	fs.readFile(filename,'ascii',function(err,data){
		if(err){
			throw err;
		}
		console.log('read finish');
		var lines=data.split("\n");
		//console.log(lines[1]);
		for(var i=1;i<lines.length;i++){
			items=lines[i].split("\t");
			items[0]=new Date(items[0]);
			cpu_info.push(items.slice(0,6));
		}
		console.log(cpu_info);
	});
}

//load_data('20120424.sty');
load_data('xx');
