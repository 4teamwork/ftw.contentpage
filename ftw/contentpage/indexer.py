from plone.indexer.decorator import indexer
from ftw.contentpage.interfaces import IContentPage


@indexer(IContentPage)
def categories(obj, **kw):
    return obj.Schema()['content_categories'].get(obj)
