from ftw.upgrade import UpgradeStep
from Products.CMFCore.utils import getToolByName


class FixPortalTypeActionTitles(UpgradeStep):

    def __call__(self):

        ttool = getToolByName(self.portal, 'portal_types')

        fti_listingblock = ttool.get('ListingBlock')
        for action in fti_listingblock._actions:
            if action.id == 'sl-dummy-dummy-dummy':
                action.title = 'Listing'
            if action.id == 'sl-dummy-dummy-gallery':
                action.title = 'Gallery'

        fti_listingblock = ttool.get('AddressBlock')
        for action in fti_listingblock._actions:
            if action.id == 'sl-dummy-dummy-dummy':
                action.title = 'Map'
