//depends: core/auth/dialog.js, apps/listing/main.js

hs.listings.views.offerDialog = hs.auth.Dialog.extend({
    // events: _.extend(hs.auth.Dialog.prototype.events, {
        
    // }),
    submit: function(e){
        this.amount = $('input[name=amount]').val();
        this.trigger('set:amount', this.amount);
        hs.auth.Dialog.prototype.events.apply(this, arguments);
    }
});
