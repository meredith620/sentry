var fs=require('fs');

function load_data(param,ecb,cb){
	fs.readdir(global.node_root+'/'+host,function(err,files){
		if(err){
			ecb(err);
		}
		var res=[];
		var count=0;
		files.filter(function(v){
			var time=Number(v.substr(0,8));
			return (Number(param.start)<=time&&time<=Number(param.end));
		}).map(function(v,i){
			count++;
			fs.readFile(global.node_root+'/'+host+'/'+v+'.sty','ascii',function(err,data){
					if(err){
						ecb(err);
					}
					res[i]=data
					count--;
					if(count<=0){
						//TODO process res[],then call cb(data)
					}
				}
			});
		});
		
	}
}

function load_data2(filename,ecb,cb){
	fs.readFile(filename,'ascii',function(err,data){
		if(err){
			ecb(err);
		}
		console.log('read finish');
		var cpu_info=[];
		var mem_info=[];
		var disk_info=[];
		var net_info=[];
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
			var data={};
			data['cpu']=cpu_info;
			data['mem']=mem_info;
			data['disk']=disk_info;
			data['net']=net_info;
			cb(data);
		}else{
			console.log(cpu_info);
		}
	});
}

exports.load_data=load_data;

//load_data('20120424.sty');
//load_data('xx');
