from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from Acquisition import aq_parent
from ftw.contentpage.config import PROJECTNAME
from ftw.contentpage.content.textblock import image_schema
from ftw.contentpage.interfaces import IAuthoritySupport
from ftw.contentpage.interfaces import ICategorizable
from ftw.contentpage.interfaces import IContentPage
from ftw.contentpage.interfaces import ITeaser
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore.permissions import View
from simplelayout.base.interfaces import IAdditionalListingEnabled
from simplelayout.base.interfaces import ISimpleLayoutCapable
from zope.interface import implements

from Products.ATContentTypes.config import HAS_LINGUA_PLONE
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone import public as atapi
else:
    from Products.Archetypes import atapi


ContentPageSchema = folder.ATFolderSchema.copy() + image_schema.copy()

schemata.finalizeATCTSchema(
    ContentPageSchema,
    moveDiscussion=False,
)
ContentPageSchema['relatedItems'].widget.visible['edit'] = 'visible'

# Protect the teaser image with a specific permission
permission = "ftw.contentpage: Edit teaser image on ContentPage"
for name in image_schema.keys():
    ContentPageSchema[name].write_permission = permission


class ContentPage(folder.ATFolder):
    """A simplelayout content page"""
    implements(IContentPage, ICategorizable, ISimpleLayoutCapable,
               IAdditionalListingEnabled, ITeaser, IAuthoritySupport)

    meta_type = "ContentPage"
    schema = ContentPageSchema
    security = ClassSecurityInfo()

    security.declarePublic('canSetDefaultPage')
    def canSetDefaultPage(self):
        return False

    security.declareProtected(View, 'getAvailableLayouts')
    def getAvailableLayouts(self):
        result = super(ContentPage, self).getAvailableLayouts()
        parent = aq_parent(aq_inner(self))
        mid = 'authorities_view'
        # authorities_view is only possible on certain points
        # For example if the ContentPage is created on plone-root.
        # This changes the Plone default behaveiour off setting the layout
        # property on child objects. We don't want this, so let's check for
        # the parent meta_type
        if parent.meta_type == self.meta_type:
            result.remove((mid, mid))
        return result

    security.declarePublic('showAddMenu')
    def showAddMenu(self):
        return False

    security.declarePublic('show_description')
    def show_description(self):
        return False

    security.declarePrivate('copyLayoutFromParent')
    def copyLayoutFromParent(self):
        """Copies the layout from the parent object if it's of the same type.
        """
        # JUST DON'T DO THIS!
        pass


atapi.registerType(ContentPage, PROJECTNAME)
