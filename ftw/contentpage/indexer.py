from DateTime import DateTime
from ftw.contentpage.config import HAS_CONTENT_LISTING_BEHAVIOR
from ftw.contentpage.interfaces import ICategorizable, IEventPage
from ftw.contentpage.interfaces import IContentPage
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.decorator import indexer
from Products.Archetypes.interfaces import IBaseObject
from simplelayout.base.interfaces import ISimpleLayoutBlock


if HAS_CONTENT_LISTING_BEHAVIOR:
    from ftw.contentpage.behaviors.content_categories import IContentCategories


@indexer(ICategorizable)
def categories(obj, **kw):
    if IBaseObject.providedBy(obj):
        return obj.Schema()['content_categories'].get(obj)
    elif IDexterityContent.providedBy(obj) and HAS_CONTENT_LISTING_BEHAVIOR:
        return [item.encode('utf-8') for item in
                IContentCategories(obj).content_categories]
    else:
        return ()


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


@indexer(IEventPage)
def start(obj):
    start = obj.start()
    if obj.getWholeDay():
        return DateTime(start.year(), start.month(), start.day(), 0, 0)
    return start


@indexer(IEventPage)
def end(obj):
    end = obj.end()
    if obj.getWholeDay():
        return DateTime(end.year(), end.month(), end.day(), 23, 59)
    return end
