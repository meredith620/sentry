var http=require('http');
var url=require('url');
var querystring=require('querystring');
var ds=require('./data');

var handler={};

function info(response,param){
	console.log(param);
	if(param.type==='cpu'){
		console.log(JSON.stringify(cpu_info));
		response.write(JSON.stringify(cpu_info));
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

function route(pathname,response,post){
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
			route(pathname,response,url.parse(request.url).query);
		});
	}).listen(8091);
	console.log('server start');
}


handler['/info']=info;
ds.load_data('20120424.sty',start);
