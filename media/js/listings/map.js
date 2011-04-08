//depends: listings/main.js

$(function(){
    if ($('.map').length){
        $('.map').each(function(){
            var map = new google.maps.Map(this, {
                zoom: 8,
                center: new google.maps.LatLng($(this).attr('data-lat'), 
                                               $(this).attr('data-lng')),
                mapTypeId: google.maps.MapTypeId.ROADMAP
            });
            $(this).data('map', map);
        });
    }
});
