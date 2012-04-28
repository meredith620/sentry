var http=require('http');
var url=require('url');
var querystring=require('querystring');
var ds=require('./data');
var fs=require('fs');
var cp=require('child_process');

//TODO grantee node_root exist
global.node_root='./node_root';
global.node=[];

function init_node(cb){
	fs.readdir(node_root,function(err,files){
		if(err){
			throw err;
		}
		global.node=files;
		console.log(files);
		cb();
	});
	fetch_data();
}

function fetch_data(){
	int count=global.node.length;
	global.node.forEach(function(value,index){
		var cmd='rync '+value+':~/islet/*.sty node_root/'+value+'/';
		cp.exec(cmd,function(err,stdout,stderr){
			if(err){
				throw err;
			}
			count--;
			if(count==0){
				console.log('fetch finish');
				setTimeout(fetch_data,1000*60*5);
			}
		});
	});
}

function node_list(response,param){
	response.end(JSON.stringify(global.node));
}

function node_add(response,param){
	console.log(param);
	if(!param.host){
		response.end();
		return;
	}
	if(param.host in global.node){
		response.end('already deployed');
		return;
	}
	deploy_islet(param.host,function(){
		global.node.push(param.host);
		response.end('add server success');
	});
}

function deploy_islet(host,cb){
	var deploy_cmd='scp -r ./islet '+host+':~/';
	var run_cmd='ssh '+host+' "cd islet ; ./catcher.py &>log &"';
	console.log(deploy_cmd);
	cp.exec(deploy_cmd,function(err,stdout,stderr){
		if(err){
			throw err;
		}
		console.log(run_cmd);
		cp.exec(run_cmd,function(err,stdout,stderr){
			if(err){
				throw err;
			}
			console.log('mkdir for host '+host);
			fs.mkdir(node_root+'/'+host,function(err){
				if(err){
					throw err;
				}
				cb();
			});
		});
	});
}


var handler={};

function info(response,param){
	console.log(param);
	//TODO change this to send a host's oneday info,change show.html to select which node ,maybe show current date is ok
	if(param.type==='cpu'){
		//console.log(JSON.stringify(cpu_info));
		response.write(JSON.stringify(cpu_info));
		response.end();
	}else if(param.type==='mem'){
		response.write(JSON.stringify(mem_info));
		response.end();
	}else if(param.type==='disk'){
		response.write(JSON.stringify(disk_info));
		response.end();
	}else if(param.type==='net'){
		response.write(JSON.stringify(net_info));
		response.end();
	}else{
		response.end('show what?');
	}
}

function render(response,file){
	var fs=require('fs');
	//current use node's fs api,TODO use do.js
	console.log('read file:'+file);
	fs.readFile(file,'ascii',function(err,data){
		if(err){
			throw err;
		}
		response.end(data);
	});
}

function route(pathname,response,get,post){
	if(pathname.match(".html")){
		render(response,pathname.slice(1));
	}else if(pathname.match(".js")){
		render(response,pathname.slice(1));
	}else if(typeof handler[pathname] ==='function'){
		if(pathname==='info'){
			handler[pathname](response,querystring.parse(get));
		}else{
			handler[pathname](response,querystring.parse(post));
		}
	}else{
		response.end('not found');
		console.log('unknow url:'+pathname);
	}
}

function start(){
	http.createServer(function(request,response){
		var post='';
		var pathname=url.parse(request.url).pathname;
		request.addListener('data',function(chunk){
			post+=chunk;
		});
		request.addListener('end',function(){
			route(pathname,response,url.parse(request.url).query,post);
		});
	}).listen(8091);
	console.log('server start');
}


handler['/info']=info;
handler['/node_list']=node_list;
handler['/node_add']=node_add;


init_node(start);
/*
init_node(function(){
	ds.load_data('20120424.sty',start);
});
*/
