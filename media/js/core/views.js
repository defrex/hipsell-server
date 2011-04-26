//depends:main.js

hs.views = new Object();

hs.views.View = Backbone.View.extend({
    _tmplContext: _.defaults(this.options || {}, {
        'MEDIA_URL': hsConst.MEDIA_URL
    }),
    render: function(){
        if (this.template) $(this.el).html(this.renderTmpl());
        return this;
    },
    renderTmpl: function(){
        if (typeof this.template == 'undefined') 
            throw('must define dialog template');
        var context = _.clone(this._tmplContext);
        if (this.model)
            context = _.extend(context, this.model.toJSON());
        return ich[this.template](context);
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
                                        'num': now.getMinutes() - date.getMinutes()};
                            }else{
                                if (date.getSeconds() < now.getSeconds()){
                                    return {'text': 'Seconds ago', 
                                            'num': now.getSeconds() - date.getSeconds()};
                                }else{
                                    return {'text': 'just now', 'num': 0};
                                }
                            }
                        }
                    }
                }
            }
        }else{
            hs.log('bad date');
            hs.log(date);
        };
    }
});

hs.views.Page = hs.views.View.extend({
    id: 'main',
});

hs.views.Dialog = hs.views.View.extend({
    el: $('#dialog')[0],
    buttons: {
        "OK": function(){this.trigger('click:ok').close();},
        "Cancel": function(){this.trigger('click:cancel').close();}
    },
    buttonBind: function(){
        _.each(this.buttons, _.bind(function(value, key){
            if (_.isFunction(value))
                this.buttons[key] = _.bind(value, this);
        }, this));
    },
    render: function(){
        $('body').append(this.el);
        this.buttonBind();
        $(this.el).html(this.renderTmpl()).dialog({
            modal: true,
            buttons: this.buttons
        });
        return this;
    },
    close: function(){return this.remove()},
    remove: function(){
        $(this.el).dialog('close').remove();
        return this;
    }
});

hs.views.FormDialog = hs.views.Dialog.extend({
    buttons: {
        "Submit": function(){this.$('form').submit();},
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
