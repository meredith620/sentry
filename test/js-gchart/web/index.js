var http=require('http');
var url=require('url');
var querystring=require('querystring');

var handler={};

function render(response,file){
	var fs=require('fs');
}

function route(pathname,response,post){
	if(pathname.match(".html")){
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
			route(pathname,response,post);
		});
	}).listen(3333);
	console.log('server start');
}

//info?type=cpu
handler['/info']=info;
start();
//add a job sched
