//depends: jquery-1.5.1.js

var rl = new Object();

rl.log = function(){
    if (window.console && typeof console.log === "function")
        console.log.apply(console, arguments);
}
