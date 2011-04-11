//depends: lib/jquery.js, lib/jquery-ui.js, lib/json2.js

var hs = new Object();

hs.log = function(){
    if (window.console && typeof console.log === "function")
        console.log.apply(console, arguments);
}
