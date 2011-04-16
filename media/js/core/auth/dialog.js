//depends: main.js, core/auth/dialog.tmpl, core/views.js

hs.auth = hs.auth || new Object();

hs.auth.Dialog = hs.views.View.extend({
    id: dialog,
    events: {
        'submit form': 'submit',
        'click a.password': 'showPassword',
        'click a.cancel-password': 'hidePassword'
    },
    render: function(){
        $('body').append(this.el);
        $(this.el).html(ich.authDialog()).dialog({
            modal: true,
            buttons: {
                "Enter": function() {$(this).children('form').submit();},
                "Cancel": function(){$(this).dialog('close');}
            }
        });
        return this;
    },
    submit: function(e){
        e.preventDefault();
        var email = $('input[name=email]').val();
        this.trigger('set:email', [email]);
    },
    showPassword: function(e){
        e.preventDefault();
        this.$('a.password').hide(200);
        this.$('label.password').show(200);
    },
    hidePassword: function(e){
        e.preventDefault();
        this.$('label.password').hide();
        this.$('a.password').show(200);
    },
    remove: function(){
        $(this.el).dialog('close').remove();
    }
});
