jq(document).ready(function(){
    jq('.portletArchiveListing .year span.yearnumber').click(function() {
        jq(this).parent().toggleClass('expanded');
        jq(this).parent().children('ul').slideToggle();
     });

});
