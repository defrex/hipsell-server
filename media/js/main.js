//depends: jquery-1.5.1.js

var hs = new Object();

hs.log = function(){
    if (window.console && typeof console.log === "function")
        console.log.apply(console, arguments);
}
