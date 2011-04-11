//depends: main.js, auth.js

hs.api = function(path, method, data, clbk){
    if (typeof method == 'object'){
        clbk = data;
        data = method;
        method = 'POST';
    }else if ($.isFunction(method)){
        clbk = method;
        method = 'GET';
        data = undefined;
    }
    if ($.isFunction(data)){
        clbk = data;
        data = undefined;
    }

    hs.auth.authenticated(function(){
        $.ajax({
            url: path,
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(data),
            beforeSend: function(jqXHR){
                jqXHR.setRequestHeader('Token', hs.auth.token);
            },
            complete: function(data){
                if (clbk) clbk.call(this, data, this.status);
            }
        });
    });
};

$(document).bind('ajaxError', function(e, jqXHR){
    if (jqXHR.status == 500){
        var erframe = document.createElement('iframe');
        $('body').append(erframe);
        $(erframe).css('position', 'absolute')
            .css('top', '50px').css('left', '50%')
            .css('width', '700px').css('height', '700px')
            .css('marginLeft', '-350px')
            .attr('id', 'errorframe');
        var doc = erframe.document;
        if (erframe.contentDocument)// for moz
            doc = erframe.contentDocument;
        doc.open();
        doc.writeln(jqXHR.responseText);
        doc.close();
        var close = $('<a href="#" id="errorclose">X</a>');
        $('body').append(close);
        close.css('position', 'absolute')
            .css('top', '40px').css('left', '50%')
            .css('marginLeft', '360px')
            .click(function(e){
                $('#errorframe').remove();
                close.remove();
            });
    }
});

