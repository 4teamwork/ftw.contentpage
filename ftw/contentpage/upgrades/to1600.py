from ftw.upgrade import UpgradeStep
from zope.dottedname.resolve import resolve
from zope.interface import noLongerProvides
from ftw.upgrade.step import LOG


INTERFACE_DOTTENAME = 'ftw.contentpage.interfaces.IOrgUnitMarker'


class FixMarkerInterfaces(UpgradeStep):

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.contentpage.upgrades:1600', steps=['rolemap', ])

        try:
            iface = resolve(INTERFACE_DOTTENAME)
            self.migrate_interface(iface)
        except ImportError:
            LOG.warn('The interface {0} does no longer exists'.format(
                INTERFACE_DOTTENAME))

    def migrate_interface(self, iface):
        query = {'object_provides': INTERFACE_DOTTENAME}
        msg = 'Migrate IOrgUnitMarker to IAuthority'

        for obj in self.objects(query, msg):
            noLongerProvides(obj, iface)
            obj.Schema()['mark_as_authority'].set(obj, True)
            obj.reindexObject(idxs=['object_provides'])
