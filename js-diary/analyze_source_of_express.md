

目录
=========

[TOC]

express目录结构
------

首先我们来分析express目录的结构，假定你已经使用npm把express安装好了。
使用命令查询nodejs包的默认安装目录在哪：

```
$ npm root
  /home/user/node_modules`
$ ls /home/user/node_modules/
  express  ejs
```

一般如果没有使用root权限，npm安装的包都在所属用户家目录下名为 **node_modules** 的文件夹中。
查看express包目录的结构如下：

```

├── express
│   ├── index.js
│   ├── Readme.js
│   ├── lib
│   │   ├── express.js
│   │   ├── .....
│   │   └── .....
│   ├── node_modules
│   │   ├── anothermodule
│   │   ├── .....
│   │   └── .....

```
我们发现还有一个也叫 node_modules 的包，这个包中存储了express依赖的其他库，lib文件夹存放了express的源码。express的主文件为 **index.js** ，主要是导出lib文件夹中express.js文件中的接口，其内容如下：

```javascript
module.exports = require('./lib/express');
```

####require语法的介绍
require真正导入的是module.exports对象，而非exports，exports是对module.exports的引用，即
`exports.name = "my name";` 因为两者引用的是同一个对象，故而此时 `module.exports.name == exports.name;`

module.exports初始化是一个 `{}` 空对象，所以如果我们在文件中对exports重新赋值，因为exports对module.exports的指向已经改变，exports已经指向了一个新对象，而require真正导出的是module.exports对象。

如果你想给module.exports赋一个新的对象，旨在让`var express = require('express.js')`时，让express直接引用那个对象，而不是类似`main.express; main.run; main.go;`的形式，你可以这么做：

```javascript
//  /lib/express.js
exports = module.exports = createApplication;
exports.application = proto;
exports.request = req;
exports.response = res;

//  index.js
module.exports = require('./lib/express');

// yourapp.js
var express = require("express");
var app = express();
```

因为上面将module.exports对象重新赋值了，但exports引用的还是老对象。而你可能又想传递更多的对象，那么你可以这样将exports重新指向为新对象。而你查看源码可以发现，createAppication不是一个函数吗？给函数赋值属性？别忘了，函数也是一个对象，继承自Function类型。而且解释器执行的时候一讲函数提升，函数便会自动拥有一个 Function.prototype 属性。因此下面的语法完全正确：

```javascript
function create(){
  return "str...";
}

create.age = 22;
create.country = "china";

create()
create.age

```
注意：函数有一些属性的名称是保留字，不应该乱使用，比如function.name是函数的名称，其特性被设置为不可枚举、只读，还有最熟悉的function.prototype等等。


####createApplication函数
通过上面的介绍我们知道 `var express = require("express")` 实际上express引用的就是 express.js中的函数createApplication，这个文件又额外把一些对象当做函数的属性赋值给了函数。
先来看看这个函数：

```javascript
var EventEmitter = require('events').EventEmitter;
var mixin = require('merge-descriptors');
var proto = require('./application');
var req = require('./request');
var res = require('./response');

function createApplication() {
  var app = function(req, res, next) {
    app.handle(req, res, next);
  };

  mixin(app, EventEmitter.prototype, false);
  mixin(app, proto, false);

  app.request = { __proto__: req, app: app };
  app.response = { __proto__: res, app: app };
  app.init();
  return app;
}
```

很奇怪的样子，安装官方文档是的使用方法，app应该是一个实例或是一个对象，用于`get, route, post`等方法。但createAppication函数返回了一个app对象，这个对象在函数里又指向了另一个匿名函数。先不去管那个匿名函数，`app.get app.post` 等方法从哪里来？答案就在 **mixin** 函数运行后！
mixin变量引用的是另外一个库 merge-descriptors，这个库在express文件夹中的node_modules文件夹可找到，代码很简单都在其index.js文件中：

```javascript
// merge-descriptors/index.js
module.exports = merge

var hasOwnProperty = Object.prototype.hasOwnProperty

function merge(dest, src, redefine) {
  if (!dest) {
    throw new TypeError('argument dest is required')
  }

  if (!src) {
    throw new TypeError('argument src is required')
  }

  if (redefine === undefined) {
    // Default to true
    redefine = true
  }

  Object.getOwnPropertyNames(src).forEach(function forEachOwnPropertyName(name) {
    if (!redefine && hasOwnProperty.call(dest, name)) {
      // Skip desriptor
      return
    }

    // Copy descriptor
    var descriptor = Object.getOwnPropertyDescriptor(src, name)
    Object.defineProperty(dest, name, descriptor)
  })

  return dest
}
```
因此mixin函数可传入三个参数 dest, src, redefine，目标函数，源函数，是否需要重新定义。


















