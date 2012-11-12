from AccessControl import ClassSecurityInfo
from ftw.contentpage import _
from ftw.contentpage.config import PROJECTNAME
from ftw.contentpage.interfaces import IListingBlock
from simplelayout.base.interfaces import ISimpleLayoutBlock
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from zope.i18n import translate
from zope.interface import implements

from Products.ATContentTypes.config import HAS_LINGUA_PLONE
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone import public as atapi
else:
    from Products.Archetypes import atapi


schema = atapi.Schema((
    atapi.BooleanField(
        'showTitle',
        schemata='default',
        default=True,
        widget=atapi.BooleanWidget(
        label=_(u'label_show_title',
                default=u'Show Title'))),
))

listing_block_schema = folder.ATFolderSchema.copy() + schema.copy()

schemata.finalizeATCTSchema(
    listing_block_schema,
    folderish=True,
    moveDiscussion=False,
)


listing_block_schema['excludeFromNav'].default = True
listing_block_schema['excludeFromNav'].visible = -1
listing_block_schema['title'].required = False
listing_block_schema['title'].default_method = 'getDefaultTitle'


class ListingBlock(folder.ATFolder):
    """A listing block for simplelayout"""
    implements(IListingBlock, ISimpleLayoutBlock,)

    meta_type = "ListingBlock"
    schema = listing_block_schema
    security = ClassSecurityInfo()

    security.declarePublic('canSetDefaultPage')
    def canSetDefaultPage(self):
        return False

    security.declarePrivate('getDefaultTitle')
    def getDefaultTitle(self):
        return translate(_(u'label_default_downloads',
                 default=u'Downloads'))


atapi.registerType(ListingBlock, PROJECTNAME)
