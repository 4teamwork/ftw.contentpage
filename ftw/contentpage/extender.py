from zope.component import adapts
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import KeywordWidget
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from ftw.contentpage import _
from ftw.contentpage.interfaces import ICategorizable


class CategoriesField(ExtensionField, LinesField):
    """A reference field to store object topic"""


class CategoriesExtender(object):
    adapts(ICategorizable)
    implements(IOrderableSchemaExtender)

    fields = [CategoriesField(
        'categories',
        multiValued=True,
        searchable=False,
        accessor='getCategories',
        roleBasedAdd=True,
        widget=KeywordWidget(
            label=_(u'label_categories', default=u'Categories'),
            description=_(u'help_tags',
                          default=u'Category for contentlisting'),
        ),
    ), ]

    def __init__(self, context):
        self.context = context
    #     self.portal = getUtility(IPloneSiteRoot)
    #     pp = getToolByName(self.context,'portal_properties')
    #     tickParents= getattr(getattr(pp,'egov.classification_properties',pp),'tickAllParents',False)
    #     self.cs = queryUtility(IClassificationItem)
    #     rootpath = getattr(self.cs.getCLProperties(self.portal),'rootpath','/')
    #     self.fields[0].widget.rootpath = rootpath
    #     self.fields[0].widget.tickAllParents = tickParents

    def getFields(self):
        return self.fields
        # portal_type = getattr(self.context, 'portal_type', None)
        # if portal_type in getattr(self.cs.getCLProperties(self.portal),'classifiabletypes',[]):
        #     return self.fields
        # return []

    def getOrder(self, original):
        #do nothing, we use this later
        return original





