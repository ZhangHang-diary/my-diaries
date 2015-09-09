var aQuery = function(selector, context) {
       return aQuery.prototype.init();
}; 
// 没有 new 此时调用了 init, init的 this 指向了 aQuery.prototype


aQuery.prototype = {
    init: function() {
        this.age = 18;
        return this;
    },
    sayName: function() { return "sayName ..."; },
    sayAge: function(){ return this.age + " years old."; },
    age: 20
}

aQuery() == aQuery.prototype;   //true

aQuery().__proto__;   // 其实是 aQuery.prototype 的 [[prototype]] 指向了 Object{}
aQuery.prototype instanceof Object        // true
aQuery().__proto__ == Object.prototype;   // true


aQuery().age;          // 18
aQuery().sayAge();    // "18 years old."





// ####################################################################################


var aQuery = function(selector, context) {
       return new aQuery.prototype.init();
}; 
// 有 new 生成了实例，this 指向了实例
// init在没有修复原型的情况下，默认的原型指向了 Object {}

aQuery.prototype = { 
    init: function() {
        this.age = 18;
        return this;
    },
    sayName: function() { return "sayName ..."; },
    sayAge: function(){ return this.age + " years old."; },
    age: 20
}

aQuery.prototype.init.prototype = aQuery.prototype; // 修复 init构造函数的原型。


aQuery().__proto__ == aQuery.prototype;   // true
aQuery().__proto__;    // 指向 aQuery.prototype


aQuery().age;          // 18
aQuery().sayAge();     //"18 years old."



// ####################################################################################



function sName(){ 
  var variable = "sName variable..."
  return function (){
    return this.variable + " sayName ...";
  }
}

var variable = "window var";

sName()();  // "window var sayName ..."

var s = sName();
s();     // "window var sayName ..."


// ####################################################################################



