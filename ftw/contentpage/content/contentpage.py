from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from ftw.contentpage.config import PROJECTNAME
from ftw.contentpage.interfaces import IContentPage
from zope.interface import implements
from simplelayout.base.interfaces import ISimpleLayoutCapable

from Products.ATContentTypes.config import HAS_LINGUA_PLONE
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone import public as atapi
else:
    from Products.Archetypes import atapi


ContentPageSchema = folder.ATFolderSchema.copy()

schemata.finalizeATCTSchema(
    ContentPageSchema,
    folderish=True,
    moveDiscussion=False,
    )


class ContentPage(folder.ATFolder):
    """A simplelayout content page"""
    implements(IContentPage, ISimpleLayoutCapable)

    meta_type = "ContentPage"
    schema = ContentPageSchema

atapi.registerType(ContentPage, PROJECTNAME)
