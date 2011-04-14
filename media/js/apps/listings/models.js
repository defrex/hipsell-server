//depends: apps/listings/main.js

hs.listings.models = new Object();

hs.listings.models.Listing = Backbone.Model.extend({
    
});


hs.listings.models.ListingSet = Backbone.Collection.extend({
    model: hs.listings.models.Listing
});
