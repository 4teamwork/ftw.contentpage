function displaySelectedTeaserLinkWidget() {
    selected_link = $('#teaserSelectLink input:checked').val();
    reference = $('.field[data-fieldname=teaserReference]');
    url = $('.field[data-fieldname=teaserExternalUrl]');
    reference.hide();
    url.hide();
    if (selected_link == 'extern') url.show();
    if (selected_link == 'intern') reference.show();
}

$(function() {
    displaySelectedTeaserLinkWidget();
    $('#teaserSelectLink input').change(displaySelectedTeaserLinkWidget);
});
