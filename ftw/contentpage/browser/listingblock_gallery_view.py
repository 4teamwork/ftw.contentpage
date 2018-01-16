from ftw.colorbox.interfaces import IColorboxSettings
from plone.app.imaging.utils import getAllowedSizes
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import getUtility


class ListingBlockGalleryView(BrowserView):
    """Block representation of ListingBlock"""

    @property
    def _build_query(self):
        query = {}
        path = '/'.join(self.context.getPhysicalPath())
        query['path'] = {'query': path, 'depth': 1}
        query['portal_type'] = ['Image']
        query['sort_on'] = self.context.getSortOn()
        query['sort_order'] = self.context.getSortOrder()
        return query

    def get_images(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(self._build_query)
        return [brain.getObject() for brain in brains]

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
