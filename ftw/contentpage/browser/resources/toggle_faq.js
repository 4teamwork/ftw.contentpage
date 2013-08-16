jQuery(function($){
  $('.faqtitle').live("click",function(e){
    e.preventDefault();
    var parentItem = $(this).closest('.FAQWrapper');
    var meetingBody = $('#'+parentItem.attr('id') + ' .faqcontent');

    if (meetingBody.css('display') != 'none'){
      $('#'+parentItem.attr('id') + ' .faqcontent').hide('blind', 100);
      $('#'+parentItem.attr('id') + ' .faqtitle .toggleImage').attr('src',portal_url+'/++resource++ftw.contentpage.resources/arrow_right.png');
    }
    else {
      $('#'+parentItem.attr('id') + ' .faqcontent').show('blind', 100);
      $('#'+parentItem.attr('id') + ' .faqtitle .toggleImage').attr('src',portal_url+'/++resource++ftw.contentpage.resources/arrow_down.png');
    }


  }).children('.sl-actions').click(function(event) {event.stopPropagation();});
});
