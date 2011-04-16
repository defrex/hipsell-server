//depends:main.js

hs.views = new Object();

hs.views.View = Backbone.View.extend({
    _tmplContext: _.defaults(this.options || {}, {
        'MEDIA_URL': hsConst.MEDIA_URL
    }),
    render: function(){
        $(this.el).html(this.renderTmpl());
    },
    renderTmpl: function(){
        if (typeof this.template == 'undefined') 
            throw('must define dialog template');
        return ich[this.template](_.extend(this._tmplContext, this.model.toJSON()));
    },
    since: function(date){
        if (!(date instanceof Date)) date = new Date(date);
        var now = new Date();
        
        if (date < now){
            if (date.getFullYear() < now.getFullYear()){
                return {'text': 'Years ago', 'num': now.getFullYear() - date.getFullYear()};
            }else{
                if (date.getMonth() < now.getMonth()){
                    return {'text': 'Months ago', 
                            'num': now.getMonth() - date.getMonth()};
                }else{
                    if (date.getDate() < now.getDate()){
                        return {'text': 'Days ago', 
                                'num': now.getDate() - date.getDate()};
                    }else{
                        if (date.getHours() < now.getHours()){
                            return {'text': 'Hours ago', 
                                    'num': now.getHours() - date.getHours()};
                        }else{
                            if (date.getMinutes() < now.getMinutes()){
                                return {'text': 'Minutes ago', 
                                        'num': now.getMinutes() - date.getMinutess()};
                            }else{
                                return {'text': 'just now', 'num': 0};
                            }
                        }
                    }
                }
            }
        }
    }
});

hs.views.Page = hs.views.View.extend({
    id: 'main',
});

hs.views.Dialog = hs.views.View.extend({
    id: dialog,
    buttons: {
        "OK": function(){this.trigger('click:ok').close();},
        "Cancel": function(){this.trigger('click:cancel').close();}
    },
    render: function(){
        $('body').append(this.el);
        $(this.el).html(this.renderTemplate()).dialog({
            modal: true,
            buttons: _.bindAll(this.buttons, this)
        });
        return this;
    },
    close: function(){this.remove();},
    remove: function(){
        $(this.el).dialog('close').remove();
    }
});

hs.views.FormDialog = hs.views.Dialog.extend({
    buttons: {
        "Submit": function() {this.$('form').submit();},
        "Cancel": function(){this.trigger('click:cancel').close();}
    },
    events: {
        'submit form': 'submit'
    },
    submit: function(e){
        e.preventDefault();
        this.trigger('submit').close();
    }
});
