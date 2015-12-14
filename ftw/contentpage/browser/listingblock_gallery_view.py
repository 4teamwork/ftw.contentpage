from ftw.colorbox.interfaces import IColorboxSettings
from plone.app.imaging.utils import getAllowedSizes
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from zope.component import getUtility


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

    def get_image_large_url(self, img):
        img_url = img.absolute_url()

        registry = getUtility(IRegistry)
        colorbox_settings = registry.forInterface(IColorboxSettings)

        if colorbox_settings.image_size:
            scales = img.restrictedTraverse('@@images')
            scaled = scales.scale('image', scale=colorbox_settings.image_size)

            if scaled:
                return scaled.url

        return img_url
