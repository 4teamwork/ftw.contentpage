from plone.indexer.decorator import indexer
from ftw.contentpage.interfaces import ICategorizable


@indexer(ICategorizable)
def categories(obj, **kw):
    return obj.Schema()['content_categories'].get(obj)
