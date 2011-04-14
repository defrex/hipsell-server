//depends: lib/main.js

var hs = new Object();

hs.log = function(){
    if (window.console && typeof console.log === "function")
        console.log.apply(console, arguments);
}
