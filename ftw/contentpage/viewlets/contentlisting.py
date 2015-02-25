from ftw.contentpage.config import HAS_CONTENT_LISTING_BEHAVIOR
from ftw.contentpage.interfaces import ISummaryListingEnabled
from plone.app.layout.viewlets import ViewletBase
from plone.dexterity.interfaces import IDexterityContent
from plone.memoize import instance
from Products.Archetypes.interfaces import IBaseObject
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


if HAS_CONTENT_LISTING_BEHAVIOR:
    from ftw.contentpage.behaviors.content_categories import IContentCategories


class ContentListingViewlet(ViewletBase):
    """Lists content by categories"""
    def render(self):
        if ISummaryListingEnabled.providedBy(self.view):
            return ViewPageTemplateFile('content_summary_listing.pt')(self)
        return ViewPageTemplateFile('contentlisting.pt')(self)

    def available(self):
        return bool(self.get_content())

    @instance.memoize
    def get_content(self):
        query = {
            'sort_on': 'sortable_title',
            'object_provides': 'ftw.contentpage.interfaces.ICategorizable'}
        contents = self.context.getFolderContents(contentFilter=query,
                                                  full_objects=True)
        return self._create_resultmap(contents)

    def _create_resultmap(self, contents=None):
        resultmap = {}
        if not contents:
            return []
        for obj in contents:
            if IBaseObject.providedBy(obj):
                categories = obj.Schema()['content_categories'].get(obj)
            elif IDexterityContent.providedBy(obj) and HAS_CONTENT_LISTING_BEHAVIOR:
                categories = [item.encode('utf-8') for item in
                              IContentCategories(obj).content_categories]

            for cat in categories:
                if cat not in resultmap:
                    resultmap[cat] = []
                resultmap[cat].append((obj.title_or_id(),
                                       obj.absolute_url(),
                                       obj.Description()))

        items = resultmap.items()
        items.sort(key=lambda x: x[0].lower())
        return items
