var http=require('http');
var url=require('url');
var querystring=require('querystring');
var ds=require('./data');
var fs=require('fs');
var cp=require('child_process');

//TODO grantee node_root exist
global.node_root='./node_root';
global.node=[];
var handler={};

function init_node(cb){
	fs.readdir(node_root,function(err,files){
		if(err){
			throw err;
		}
		global.node=files;
		console.log('node:');
		console.log(files);
		fetch_data();
		cb();
	});
}

function fetch_data(){
	var count=global.node.length;
	console.log('fetch');
	console.log(count);
	global.node.forEach(function(value,index){
		var cmd='rsync supertool@'+value+':~/islet/*.sty node_root/'+value+'/';
		console.log('fetch '+cmd);
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
	console.log(global.node);
	console.log(param.host);
	if(global.node.indexOf(param.host)!=-1){
		response.statusCode=301;
		response.setHeader('Location','/all.html');
		response.end('already deployed');
		return;
	}
	deploy_islet(param.host,function(){
		global.node.push(param.host);
		response.statusCode=301;
		response.setHeader('Location','/all.html');
		response.end('add server success');
	});
}

function deploy_islet(host,cb){
	var deploy_cmd='scp -r ./islet '+host+':~/';
	var run_cmd='ssh supertool@'+host+' "cd islet ; ./catcher.py &>log &"';
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



function info(response,param){
	console.log(param);
	//param.host='100.mzhen.cn';
	var today=new Date();
	if(!/\d{8}/.test(param.end)){
		param.end=String(today.getFullYear());
		param.end+=today.getMonth()+1<10?'0':'';
		param.end+=(today.getMonth()+1);
		param.end+=today.getDate()<10?'0':'';
		param.end+=today.getDate();
	}
	if(!/\d{8}/.test(param.start)){
		param.end=String(today.getFullYear());
		param.end+=today.getMonth()+1<10?'0':'';
		param.end+=(today.getMonth()+1);
		param.end+=today.getDate()<10?'0':'';
		param.end+=today.getDate();
		param.start=param.end;
	}
	console.log(param);
	
	function ecb(err){
		response.end();
		console.log(err);
		throw err;
	}
	function cb(data){
		response.end(JSON.stringify(data));
		//console.log(JSON.stringify(data));
	}
	ds.load_data(param,ecb,cb);
}

function render(response,file,regex,target){
	var fs=require('fs');
	//current use node's fs api,TODO use do.js
	console.log('read file:'+file);
	fs.readFile(file,'ascii',function(err,data){
		if(err){
			throw err;
		}
		if(target && regex){
			data=data.replace(regex,target)
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
		handler[pathname](response,querystring.parse(post));
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
handler['/node_detail']=function(response,param){
	if(global.node.indexOf(param.host)!=-1){
		render(response,'detail.html',/__HOST__/g,param.host);
	}else{
		response.end('param error');
	}
};

init_node(start);
