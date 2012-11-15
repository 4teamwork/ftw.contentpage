from collective.geo.settings.interfaces import IGeoSettings
from collective.geo.settings.interfaces import IGeoFeatureStyle
from ftw.contentpage.config import INDEXES
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
import logging

LOGGER = logging.getLogger('ftw.contentpage')


def add_catalog_indexes(context):
    """Method to add our wanted indexes to the portal_catalog.

    @parameters:

    When called from the import_various method below, 'context' is
    the plone site and 'logger' is the portal_setup logger.  But
    this method can also be used as upgrade step, in which case
    'context' will be portal_setup and 'logger' will be None.
    """

    catalog = getToolByName(context, 'portal_catalog')
    indexes = catalog.indexes()
    # Specify the indexes you want, with ('index_name', 'index_type')
    indexables = []
    for name, meta_type in INDEXES:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            LOGGER.info("Added %s for field %s.", meta_type, name)
    if len(indexables) > 0:
        LOGGER.info("Indexing new indexes %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


def georef_settings(context):
    """Import step to set up AddressBlock as georeferenceable type in
    colllective.geo.settings.

    This just adds a registry entry, but it can't be done through registry.xml
    because at that point the AddressBlock type hasn't been registered yet.
    """

    registry = getUtility(IRegistry)
    geo_content_types = registry.forInterface(
        IGeoSettings).geo_content_types
    registry.forInterface(
        IGeoFeatureStyle).map_viewlet_position = 'fake-manager'
    if not 'AddressBlock' in geo_content_types:
        geo_content_types.append('AddressBlock')


def import_various(context):
    """Import step for configuration that is not handled in xml files.
    """
    # Only run step if a flag file is present
    if context.readDataFile('ftw.contentpage.setuphandlers.txt') is None:
        return
    site = context.getSite()
    add_catalog_indexes(site)
    georef_settings(site)
