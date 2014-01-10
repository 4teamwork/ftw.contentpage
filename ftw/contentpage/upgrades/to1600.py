from ftw.contentpage.interfaces import IOrgUnitMarker
from ftw.upgrade import UpgradeStep
from zope.interface import noLongerProvides


class FixMarkerInterfaces(UpgradeStep):

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.contentpage.upgrades:1600', steps=['rolemap', ])

        query = {'object_provides': IOrgUnitMarker.__identifier__}
        msg = 'Migrate IOrgUnitMarker to IListingMarker'

        for obj in self.objects(query, msg):
            noLongerProvides(obj, IOrgUnitMarker)
            obj.Schema()['mark_for_listings'].set(obj, True)
            obj.reindexObject(idxs=['object_provides'])
