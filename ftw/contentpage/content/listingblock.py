from AccessControl import ClassSecurityInfo
from ftw.contentpage import _
from ftw.contentpage.config import PROJECTNAME
from ftw.contentpage.content.schema import finalize
from ftw.contentpage.interfaces import IListingBlock
from plone.registry.interfaces import IRegistry
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from simplelayout.base.interfaces import ISimpleLayoutBlock
from zope.component import getUtility, queryMultiAdapter
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

    atapi.LinesField(
        'tableColumns',
        schemata='default',
        required=True,
        default_method="getDefaultTableColumns",
        vocabulary='getColumns',
        widget=atapi.InAndOutWidget(
        label=_(u'Columns',
                default=u'Columns'))),

    atapi.StringField(
        'sortOn',
        required=True,
        default="sortable_title",
        vocabulary='getSortIndexVocabulary',
        widget=atapi.SelectionWidget(
            label=_(u'label_sort_on', default=u'Sort On'),
            description=_(u'help_sort_on', default=u''),
            format='select',
        ),
    ),

    atapi.StringField(
        'sortOrder',
        required=True,
        default="asc",
        vocabulary=[('ascending', _(u'label_ascending', default=u'Ascending')),
                    ('descending', _(u'label_descending',
                        default=u'Descending'))],
        widget=atapi.SelectionWidget(
            label=_(u'label_sort_order', default=u'Sort Order'),
            description=_(u'help_sort_order', default=u''),
            format='select',
        ),
    )

))

listing_block_schema = folder.ATFolderSchema.copy() + schema.copy()

schemata.finalizeATCTSchema(
    listing_block_schema,
    folderish=True,
    moveDiscussion=False,
)


listing_block_schema['title'].required = False
listing_block_schema['title'].default_method = 'getDefaultTitle'

finalize(listing_block_schema, hide=['description'])


class ListingBlock(folder.ATFolder):
    """A listing block for simplelayout"""
    implements(IListingBlock, ISimpleLayoutBlock,)

    meta_type = "ListingBlock"
    schema = listing_block_schema
    security = ClassSecurityInfo()

    security.declarePublic('showAddMenu')
    def showAddMenu(self):
        return False

    security.declarePublic('canSetDefaultPage')
    def canSetDefaultPage(self):
        return False

    security.declarePrivate('getDefaultTitle')
    def getDefaultTitle(self):
        registry = getUtility(IRegistry)
        return registry.get(
            'ftw.contentpage.listingblock.defaulttitle', None) or ''

    security.declarePrivate('getDefaultTableColumns')
    def getDefaultTableColumns(self):
        """ Returns the default table columns defined in registry.
        """
        registry = getUtility(IRegistry)
        return registry.get(
            'ftw.contentpage.listingblock.defaulttablecolumns',
            ('getContentType', 'Title', 'modified'))

    security.declarePrivate('getColumns')
    def getColumns(self):
        display_list = atapi.DisplayList()
        view = self.restrictedTraverse('@@block_view')
        for col in view.columns():
            display_list.add(col['column'], col['column_title'])
        return display_list

    security.declarePrivate('getSortIndexVocabulary')
    def getSortIndexVocabulary(self):
        view = queryMultiAdapter((self, self.REQUEST), name=u'block_view')
        voc = atapi.DisplayList()
        for col in view.columns():
            if 'sort_index' in col:
                voc.add(col['sort_index'], _(u'label_%s' % col['sort_index'],
                        default=col['sort_index']))
        voc.add('getObjPositionInParent', _(u'label_position_in_folder',
                default=u'Position in Folder'))
        return voc

atapi.registerType(ListingBlock, PROJECTNAME)
