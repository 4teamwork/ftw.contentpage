from Products.Five.browser import BrowserView
from plone.app.imaging.utils import getAllowedSizes


class ListingBlockGalleryView(BrowserView):
    """Block representation of ListingBlock"""

    @property
    def _build_query(self):
        query = {}
        query['portal_type'] = ['Image']
        return query

    def get_images(self):
        return self.context.listFolderContents(
            contentFilter=self._build_query)

    def _get_box_boundaries(self):
        sizes = getAllowedSizes()
        # Fallback is a plone default scale -> mini
        return sizes.get('listingblock_gallery', 'mini')
