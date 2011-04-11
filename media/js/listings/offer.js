//depends: listings/main.js, lib/jquery.tmpl.js

$(function(){
    $('#offer').click(function(){
        $('#dialog').html($('#offerTmpl').tmpl()).dialog({
            modal: true,
            buttons: {
                "Bid": function() {
                    
                },
                "Cancel": function() {
                    $(this).dialog( "close" );
                }
            }
        });
    });
});
