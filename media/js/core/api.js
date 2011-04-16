//depends: main.js, core/auth/main.js

hs.api = function(path, method, data, clbk, context){
    if (typeof method == 'object'){
        context = clbk;
        clbk = data;
        data = method;
        method = 'POST';
    }else if (_.isFunction(method)){
        context = data;
        clbk = method;
        method = 'GET';
        data = undefined;
    }
    if (_.isFunction(data)){
        context = clbk;
        clbk = data;
        data = undefined;
    }
    _.bind(clbk, context);

    hs.auth.authenticated(function(){
        $.ajax({
            url: path,
            contentType: 'application/json',
            dataType: 'json',
            data: method == 'GET'? undefined: JSON.stringify(data),
            context: context,
            beforeSend: function(jqXHR){
                jqXHR.setRequestHeader('Authorization', 'Token '+hs.auth.token);
            },
            complete: function(jqXHR){
                clbk(JSON.parse(jqXHR.responseText), jqXHR.status);
            }
        });
    });
};

//hs._BackboneSync = Backbone.sync;
Backbone.sync = function(method, model, success, error){
    var methodMap = {
        'create': 'POST',
        'update': 'PUT',
        'delete': 'DELETE',
        'read': 'GET'
    };
    hs.api(model.url(), methodMap[method], model.toJSON(), function(data, status){
        if (status < 400) success(data);
        else error(data);
    });
};


$(document).bind('ajaxError', function(e, jqXHR){
    if (jqXHR.status == 500){
        var erframe = document.createElement('iframe');
        $('body').append(erframe);
        $(erframe).css({
            'position': 'absolute',
            'top': '5%', 'left': '50%',
            'width': '90%', 'height': '90%',
            'marginLeft': '-45%'
        }).attr('id', 'errorframe');
        var doc = erframe.document;
        if (erframe.contentDocument)// for moz
            doc = erframe.contentDocument;
        doc.open();
        doc.writeln(jqXHR.responseText);
        doc.close();
        var close = $('<a href="#" id="errorclose">X</a>');
        $('body').append(close);
        close.css({
            'position': 'absolute',
            'top': '0', 'right': '0',
            'padding': '5px'
        }).click(function(e){
            $('#errorframe').remove();
            close.remove();
        });
    }
});

