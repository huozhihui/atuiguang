/**
 * 验证
 */
jQuery.extend(jQuery.validator.messages, {
    required: "必填字段",
    remote: "请修正该字段",
    email: "请输入正确格式的电子邮件",
    url: "请输入合法的网址",
    date: "请输入合法的日期",
    dateISO: "请输入合法的日期 (ISO).",
    number: "请输入合法的数字",
    digits: "只能输入非负整数",  //正整数+0
    creditcard: "请输入合法的信用卡号",
    equalTo: "请再次输入相同的值",
    accept: "请输入拥有合法后缀名的字符串",  //输入拥有合法后缀名的字符串（上传文件的后缀）
    maxlength: $.validator.format("请输入一个长度最多是 {0} 的字符串"),
    minlength: $.validator.format("请输入一个长度最少是 {0} 的字符串"),
    rangelength: jQuery.validator.format("请输入一个长度介于 {0} 和 {1} 之间的字符串"),  //汉字算一个字符
    range: jQuery.validator.format("请输入一个介于 {0} 和 {1} 之间的值"),
    max: jQuery.validator.format("请输入一个最大为 {0} 的值"),
    min: jQuery.validator.format("请输入一个最小为 {0} 的值")
});

/**
 * 只能包含汉子
 */
jQuery.validator.addMethod("chinese_character", function (value, element) {
    var reg = /^[\u4e00-\u9fa5]*$/;
    return this.optional(element) || reg.test(value);
}, "只能填写汉字");


/**
 * 只能包含英文字母、数字、_和-
 */
jQuery.validator.addMethod("letter_num_underline", function (value, element) {
    var reg = /^[\a-zA-Z\_]+[\d\a-zA-Z\_\-]*$/;
    return this.optional(element) || reg.test(value);
}, "只能包含英文字母、数字、_和-");

/**
 * 只能包含英文字母、数字、.(点)、_和-
 */
jQuery.validator.addMethod("valid_os", function (value, element) {
    var reg = /^[\d\a-zA-Z\_\-\.]*$/;
    return this.optional(element) || reg.test(value);
}, "只能包含英文字母、数字、.(点)、_和-");

/**
 * 只能包含英文字母、数字加特殊符号
 * ^[a-zA-Z0-9!@#$%^&*()_+|{}?><\-\]\\[\/]*$
 */
jQuery.validator.addMethod("valid_letter_digital_symbol", function (value, element) {
    var reg = /^[a-zA-Z0-9!@#$%^&*()_+|{}?><\-\]\\[\/]*$/;
    return this.optional(element) || reg.test(value);
}, "只能包含英文字母、数字和特殊符号");


/**
 * 通用名称验证规则：
 * 只能包含中文字符、英文字母、数字、_、-、（和）,且只能以字母或_或中文开头;其中括号可以为中英文的都可以
 */
jQuery.validator.addMethod("CommonNameCN", function (value, element) {
    var reg = /^[\a-zA-Z\_\u4e00-\u9fa5]+[\d\a-zA-Z\u4e00-\u9fa5\_\-\(\)\（\）]*$/;
    return this.optional(element) || reg.test(value);
}, "只能包含中文字符、英文字母、数字、_、-、（和）,且只能以汉子字母或_开头");


/**
 * 邮政编码规则
 */
jQuery.validator.addMethod("uecZipCode", function (value, element) {
    var tel = /^[0-9]{6}$/;
    return this.optional(element) || (tel.test(value));
}, "请正确填写您的邮政编码");


/**
 * 手机号码验证
 */
jQuery.validator.addMethod("phone", function (value, element) {
    var reg = /^1[3|4|5|8]\d{9}$/;
    return this.optional(element) || (reg.test(value));
}, "请输入正确的11位手机号码");

/**
 * 手机号码或邮箱验证
 */
jQuery.validator.addMethod("phone_email", function (value, element) {
    var reg = /^1[3|4|5|8]\d{9}$/;
    var reg1 = /[a-zA-Z0-9]{1,10}@[a-zA-Z0-9]{1,5}\.[a-zA-Z0-9]{1,5}/;
    return this.optional(element) || (reg.test(value)) || (reg1.test(value));
}, "请输入正确的邮箱或手机号");

//this one requires the text "buga", we define a default message, too
$.validator.addMethod("buga", function (value) {
    return value == "buga";
}, 'Please enter "buga"!');


// this one requires the value to be the same as the first parameter
$.validator.methods.equal = function (value, element, param) {
    return value == param;
};

//$.validator.addMethod("math", function(value, element, params) {
//  return this.optional(element) || value == params[0] + params[1];
//}, $.validator.format("Please enter the correct value for {0} + {1}"));


//IP地址验证   
jQuery.validator.addMethod("ip", function (value, element) {
    return this.optional(element) || /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(value);
    // return this.optional(element) || /^(([1-9]|([1-9]\d)|(1\d\d)|(2([0-4]\d|5[0-5])))\.)(([1-9]|([1-9]\d)|(1\d\d)|(2([0-4]\d|5[0-5])))\.){2}([1-9]|([1-9]\d)|(1\d\d)|(2([0-4]\d|5[0-5])))$/.test(value);
}, "请填写正确的IP地址。");

