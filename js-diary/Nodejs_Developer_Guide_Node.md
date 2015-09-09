[toc]


##一些常用函数
util.inspect(url.parse(req.url, true))


## fs模块
fs.readFile 调用时所做的工作只是将异步式 I/O 请求发送给了操作系统,然后立即
返回并执行后面的语句,执行完以后进入事件循环监听事件。当 fs 接收到 I/O 请求完成的
事件时,事件循环会主动调用回调函数以完成后续工作。因此我们会先看到 end. ,再看到
file.txt 文件的内容。



##npm

$ npm link express  在工程目录下把全局包链接过来
./node_modules/express -> /usr/local/lib/node_modules/express

npm init     在一个空目录运行，会产生一个符合CommonJS规范的package.json文件

npm adduser  创建账号
 
npm whoami   验证是否取得了账号

npm publish   在package.json所在文件运行可发布到npm

有更新需修改版本号，重写 npm publish

npm unpublish  可取消已发布的包


##调试

node debug run.js    进入 debug interaction interpreter

//在一个终端中
$ node --debug-brk debug.js
debugger listening on port 5858
//在另一个终端中
$ node debug 127.0.0.1:5858
connecting... ok
debug> n
break in /home/byvoid/debug.js:2
1 var a = 1;
2 var b = 'world';
3 var c = function (x) {
4
console.log('hello ' + x + a);
debug>
事实上,当使用 node debug debug.js 命令调试时,只不过是用 Node.js 命令行工
具将以上两步工作自动完成而已。

###使用node-inspector调试
$ node --debug-brk=5858 run.js  
$ node-inspector
打开 http://127.0.0.1:8080/debug?port=5858


##核心模块

process.argv


process.NextTick(callback)

```javascript
function doSomething(args, callback) {
somethingComplicated(args);
callback();
}
doSomething(function onEnd() {
compute();
});


function doSomething(args, callback) {
somethingComplicated(args);
process.nextTick(callback);
}
doSomething(function onEnd() {
compute();
});
```



##http.ServerRequest

http.ServerRequest 是 HTTP 请求的信息,是后端开发者最关注的内容。它一般由
http.Server 的 request 事件发送,作为第一个参数传递,通常简称 request 或 req

HTTP 请求一般可以分为两部分:请求头(Request Header)和请求体(Requset Body)。
以上内容由于长度较短都可以在请求头解析完成后立即读取。而请求体可能相对较长,需要一定的时间传输,因此 http.ServerRequest 提供了以下3个事件用于控制请求体
传输。

>data :当请求体数据到来时,该事件被触发。该事件提供一个参数 chunk ,表示接收到的数据。如果该事件没有被监听,那么请求体将会被抛弃。该事件可能会被调用多次。


> end :当请求体数据传输完成时,该事件被触发,此后将不会再有数据到来。

>close : 用户当前请求结束时,该事件被触发。不同于 end ,如果用户强制终止了传输,也还是调用 close 。



###GET 
可用 url.parse(request.url) 来获取GET信息，因为GET请求被嵌入了URL的完整路径，

```javascript
var http = require('http');
var url = require('url');
var util = require('util');
http.createServer(function(req, res) {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end(util.inspect(url.parse(req.url, true)));
}).listen(3000);


{ search: '?name=byvoid&email=byvoid@byvoid.com',
query: { name: 'byvoid', email: 'byvoid@byvoid.com' },
pathname: '/user',
```


###POST
Node.js默认不会解析请求体，因为类似上传文件之类的请求耗时较长，因此需要手动来监听请求体事件。

```javascript
var http = require('http');
var querystring = require('querystring');
var util = require('util');


http.createServer(function(req, res) {
  var post = '';
  req.on('data', function(chunk) {
    post += chunk;
  });
  req.on('end', function() {
    post = querystring.parse(post);
    res.end(util.inspect(post));
  });
}).listen(3000);
```

在闭包中保存了请求体信息，quertstring.parse将post解析为真正的POST请求格式。




##HTTP客户端



###REST风格路由规则

所谓安全是指没有副作用,即请求不会对资源产生变动,连续访问多次所获得的结果不受访问者的影响。而幂等指的是重复请求多次与一次请求的效果是一样的,比如获取和更新操作是幂等的,这与新增不同。删除也是幂等的,即重复删除一个资源,和删除一次是一样的。

REST风格HTTP 请求的特点
请求方式    安全      幂等
GET         是       是
POST        否       否
PUT         否       是
DELETE      否       是




##部署

###判断模块是否是其他模块调用的

```javascript
if (!module.parent) {
  app.listen(3000);
  console.log("Express server listening on port %d in %s mode", app.address().port, app.settings.env);
}
```
如果为被其他模块require，则不会执行if中的语句，其他调用者需要在自身程序中listen。



###cluster

```javascript
var cluster = require('cluster');
var os = require('os');

// 获取CPU 的数量
var numCPUs = os.cpus().length;
var workers = {};

if (cluster.isMaster) {
// 主进程分支

  cluster.on('death', function (worker) {
// 当一个工作进程结束时,重启工作进程
    delete workers[worker.pid];
    worker = cluster.fork();
    workers[worker.pid] = worker;
  });
  
// 初始开启与CPU 数量相同的工作进程
  for (var i = 0; i < numCPUs; i++) {
    var worker = cluster.fork();
    workers[worker.pid] = worker;
  }
} else {

// 工作进程分支,启动服务器
  var app = require('./app');
  app.listen(3000);
}


// 当主进程被终止时,关闭所有工作进程
process.on('SIGTERM', function () {
  for (var pid in workers) {
    process.kill(pid);
  }
  process.exit(0);
});
```

cluster.js 的功能是创建与CPU 核心个数相同的服务器进程,以确保充分利用多核CPU 的资源。主进程生成若干个工作进程,并监听工作进程结束事件,当工作进程结束时,重新启动一个工作进程。分支进程产生时会自顶向下重新执行当前程序,并通过分支判断进入工作进程分支,在其中读取模块并启动服务器。通过 cluster 启动的工作进程可以直接实现端口复用,因此所有工作进程只需监听同一端口。当主进程终止时,还要主动关闭所有工作进程。


###启动脚本
run.bash
```bash
#! /bin/sh
NODE_ENV=production
DAEMON="node cluster.js"
NAME=Microblog
DESC=Microblog
PIDFILE="microblog.pid"

case "$1" in
start)
echo "Starting $DESC: "
nohup $DAEMON > /dev/null &
echo $! > $PIDFILE
echo "$NAME."
;;
stop)
echo "Stopping $DESC: "
pid='cat $PIDFILE'
kill $pid
rm $PIDFILE
echo "$NAME."
;;
esac
exit 0
```

$ ./run start
$ ./run stop

它的功能是通过 nohup 启动服务器,使进程不会因为退出终端而关闭,同时将主进程的pid 写入microblog.pid 文件。当调用结束命令时,从microblog.pid 读取 pid 的值,终止主进程以关闭服务器。


###反向代理
Nginx配置
```
server {
	listen 80;
	server_name mysite.com;
    
	location / {
	proxy_pass http://localhost:3000;
	}
}
```


" 《深入浅出Node.js》"
##



