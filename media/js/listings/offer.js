//depends: listings/main.js, lib/jquery.tmpl.js, api.js, auth.js

$(function(){
    $('#offer').click(function(){
        $('#dialog').html($('#offerTmpl').tmpl()).dialog({
            modal: true,
            buttons: {
                "Bid": function() {
                    hs.auth.setEmail($('#offerEmail input').val());
                    hs.api('/api/v1/offer/', {
                        amount: $('#offerAmount input').val(),
                        listing: CONST.listing.id
                    }, function(){
                        $(this).dialog( "close" );
                    });
                },
                "Cancel": function() {
                    $(this).dialog( "close" );
                }
            }
        });
    });
});
