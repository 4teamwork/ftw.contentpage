jQuery(function($){
    $(document).ready(function(){
        $('.portletArchiveListing .year span.yearnumber').click(function() {
            $(this).parent().toggleClass('expanded');
            $(this).parent().children('ul').slideToggle();
         });
    });
});
