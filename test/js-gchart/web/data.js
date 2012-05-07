var fs=require('fs');
function load_data(param,ecb,cb){
	fs.readdir(global.node_root+'/'+param.host,function(err,files){
		if(err){
			ecb(err);
			return;
		}
		var res=[];
		var count=0;
		files.filter(function(v){
			var time=Number(v.substr(0,8));
			return (Number(param.start)<=time&&time<=Number(param.end));
		}).map(function(v,i){
			count++;
			fs.readFile(global.node_root+'/'+param.host+'/'+v,'ascii',function(err,data){
				count--;
				if(err){
					console.log(err);
					return;
				}
				res[i]=data;
				if(count<=0){
					//process res[],then call cb(info)
					var info={cpu:[],mem:[],disk:[],net:[]};
					for (r in res){
						var lines=res[r].split('\n');
						var head=lines.shift().split('\t');
						lines.pop();
						for(l in lines){
							var items=lines[l].split('\t');
							if(items.length!=head.length){
								continue;
							}
							info.cpu.push(items.slice(0,6));
							var time=[items[0]];
							info.mem.push(time.concat(items.slice(6,11)));
							info.disk.push(time.concat(items.slice(11,18)));
							info.net.push(time.concat(items.slice(18)));
						}
					}
					cb(info);
				}
			});
		});
	});
		
}

exports.load_data=load_data;
/* for test
global.node_root='./node_root'
load_data({
	host:'100.mzhen.cn',
	start:'20120510',
	end:'20120511'
},function(err){
	console.log(err);
},
function(info){
	console.log(info);
});
*/
