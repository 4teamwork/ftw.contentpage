jQuery(function($){
  $('.faqtitle').live("click",function(e){
    e.preventDefault();
    var parentItem = $(this).closest('.FAQWrapper');
    var FAQBody = $('#'+parentItem.attr('id') + ' .faqcontent');
    $('div.open').hide(100);
    $('div.open').addClass('folded')
    $('div.open').removeClass('open')
    $('.faqtitle .itemTitle').removeClass('imgdown')
    $('.faqtitle .itemTitle').addClass('imgright')

    if (FAQBody.css('display') == 'none'){
      $('#'+parentItem.attr('id') + ' .faqcontent').show(100);
      $('#'+parentItem.attr('id') + ' .faqcontent').removeClass('folded')
      $('#'+parentItem.attr('id') + ' .faqcontent').addClass('open')
      $('#'+parentItem.attr('id') + ' .faqtitle .itemTitle').removeClass('imgright')
      $('#'+parentItem.attr('id') + ' .faqtitle .itemTitle').addClass('imgdown')
    }


  })
});
