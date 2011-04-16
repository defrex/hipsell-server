//depends: apps/listings/main.js

hs.listings.models = new Object();

hs.listings.models.Listing = Backbone.Model.extend({
    url: function(){
        return hs.API_URL+'listing/'+this.id+'/';
    }
});


hs.listings.models.ListingSet = Backbone.Collection.extend({
    model: hs.listings.models.Listing,
    url: hs.API_URL+'listing/'
});
