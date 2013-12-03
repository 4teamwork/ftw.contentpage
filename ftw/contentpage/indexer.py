from plone.indexer.decorator import indexer
from ftw.contentpage.interfaces import ICategorizable
from ftw.contentpage.interfaces import IContentPage
from simplelayout.base.interfaces import ISimpleLayoutBlock


@indexer(ICategorizable)
def categories(obj, **kw):
    return obj.Schema()['content_categories'].get(obj)


SNIPPETTEXT_FIELDS = {
    'TextBlock': [
        'text',
        'imageCaption',
    ],
    'AddressBlock': [
        'department',
        'address',
        'extraAddressLine',
        'city',
        'country',
        'phone',
        'fax',
        'email',
        'www',
    ],
}


@indexer(IContentPage)
def snippet_text(obj):
    """Text for snippets (aka highlighting) in search results."""
    text = obj.SearchableText()

    # Remove id and title
    for fieldname in ['id', 'title']:
        field = obj.getField(fieldname)
        accessor = field.getIndexAccessor(obj)
        value = accessor()
        text = text.replace(value, '', 1)

    # Include snippet text of the various block types
    block_texts = []
    for block in obj.objectValues():

        if not ISimpleLayoutBlock.providedBy(block):
            continue

        # Only add title if it's visible
        if 'showTitle' in block.Schema():
            if block.getShowTitle():
                block_texts.append(block.Title())
        else:
            block_texts.append(block.Title())

        # Add block-specific fields
        for fieldname in SNIPPETTEXT_FIELDS.get(block.portal_type, []):
            field = block.getField(fieldname)
            accessor = field.getIndexAccessor(block)
            block_texts.append(accessor())

    text += ' '.join(block_texts)

    return text
