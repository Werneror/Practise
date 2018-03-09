var util = require('util');


// 用 util.inherits 实现对象间原型继承
// 只继承原型中定义的属性和方法，不继承构造函数内部创造的属性和方法
// 而 console.log 却只显示构造函数内部创造的属性和方法
console.log("\n\n用 util.inherits 实现对象间原型继承：");
function Base(){
    this.name = 'base';
    this.base = 1991;
    this.sayHello = function() {
        console.log("Hello " + this.name);
    };
}
Base.prototype.age = 50;
Base.prototype.showName = function() {
    console.log(this.name);
};
function Sub(){
    this.name = 'sub';
}

util.inherits(Sub, Base);
var objBase = new Base();
objBase.showName();
objBase.sayHello();
console.log(objBase.age);
console.log(objBase);
var objSub = new Sub();
objSub.showName();
//objSub.sayHello();
console.log(objSub.age);
console.log(objSub);


// 使用 util.inspect 输出对象
// 参数 object 是要转换的对象。
// 参数 showHidden 可选，若为 true，将会输出更多隐藏信息
// 参数 depth=2 可选，表示最大递归的层数，指定为 null 表示将不限递归层数完整遍历对象
// 参数 color 可选，若值为 true，输出格式将会以ANSI 颜色编码，通常用于在终端显示更漂亮的效果
console.log("\n\n使用 util.inspect 输出对象：");
function Person(){
    this.name = 'byvoid';
    this.toString = function() {
        return this.name;
    };
}
var obj = new Person();
console.log(util.inspect(obj));
console.log(util.inspect(obj, true, null, true));


// 使用 util.isArray 判断对象是否是数组
console.log("\n\n使用 util.isArray 判断对象是否是数组：");
console.log("[] 是数组吗？" + util.isArray([]));
console.log("new Array 是数组吗？" + util.isArray(new Array));
console.log("new Array() 是数组吗？" + util.isArray(new Array()));
console.log("{} 是数组吗？" + util.isArray({}));
console.log("12 是数组吗？" + util.isArray(12));


// 使用 util.isRegExp(object) 判断对象是否是正则表达式
console.log("\n\n使用 util.isRegExp(object) 判断对象是否是正则表达式：");
console.log("/some regexp/ 是正则表达式吗？" + util.isRegExp(/some regexp/));
console.log("'another regexp' 是正则表达式吗？" + util.isRegExp('another regexp'));
console.log("new RegExp('another regexp') 是正则表达式吗？" + util.isRegExp(new RegExp('another regexp')));
console.log("{} 是正则表达式吗？" + util.isRegExp({}));
console.log("true 是正则表达式吗？" + util.isRegExp(true));


// 使用 util.isDate(object) 判断对象是否是正则表达式
console.log("\n\n使用 util.isDate(object) 判断对象是否是日期：");
console.log("new Date 是日期吗？" + util.isDate(new Date));
console.log("new Date() 是日期吗？" + util.isDate(new Date()));
console.log("Date() 是日期吗？" + util.isDate(Date()));
console.log("{} 是日期吗？" + util.isDate({}));


// 使用 util.isError(object) 判断对象是否是错误对象
console.log("\n\n使用 util.isError(object) 判断对象是错误对象：");
console.log("new Error() 是错误对象吗？" + util.isError(new Error()));
console.log("{name: 'error', message: 'an error occurred'} 是错误对象吗？" + util.isError({name: 'error', message: 'an error occurred'}));
