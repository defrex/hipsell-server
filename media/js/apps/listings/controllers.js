//depends: controller.js, apps/listings/models.js

hs.regController('listings', Backbone.Controller.extend({
    routes: {
        '/listings/:id/': 'listing'
    },
    listing: function(id){
        hs.log('routed to listing');
        var listings = new hs.listings.models.ListingSet(),
            listing = listings.get(id);
        hs.log(listing);
    }
}));

