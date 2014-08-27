from ftw.contentpage.interfaces import IAddressBlock
from ftw.upgrade import UpgradeStep
from Products.CMFCore.utils import getToolByName


class ConvertAddressblockToHTML(UpgradeStep):

    def __call__(self):
        portal_transforms = getToolByName(self, 'portal_transforms')

        query = {'object_provides': IAddressBlock.__identifier__}
        for obj in self.catalog_unrestricted_search(query, full_objects=True):
            if obj.directions.getContentType() == 'text/plain':
                directions = portal_transforms.convertTo(
                    'text/html',
                    obj.getRawDirections(),
                    mimetype='text/plain').getData()
                directions = directions.replace('\r', '')
                obj.setDirections(directions)

            if obj.openingHours.getContentType() == 'text/plain':
                openingHours = portal_transforms.convertTo(
                    'text/html',
                    obj.getRawOpeningHours(),
                    mimetype='text/plain').getData()
                openingHours = openingHours.replace('\r', '')
                obj.setOpeningHours(openingHours)
