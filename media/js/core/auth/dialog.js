//depends: main.js, core/auth/dialog.tmpl, core/views.js

hs.auth = hs.auth || new Object();

hs.auth.Dialog = hs.views.FormDialog.extend({
    events: _.extend(hs.views.FormDialog.prototype.events, {
        'click a.password': 'showPassword',
        'click a.cancel-password': 'hidePassword'
    }),
    submit: function(e){
        e.preventDefault();
        this.email = $('input[name=email]').val();
        this.trigger('set:email', this.email);
        hs.views.FormDialog.prototype.events.apply(this, arguments);
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
    }
});
