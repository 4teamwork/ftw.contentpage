from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.Archetypes import atapi
from ftw.contentpage.config import PROJECTNAME
from ftw.contentpage.interfaces import IContentPage
from zope.interface import implements

ContentPageSchema = folder.ATFolderSchema.copy()

schemata.finalizeATCTSchema(
    ContentPageSchema,
    folderish=True,
    moveDiscussion=False,
    )


class ContentPage(folder.ATFolder):
    """A simplelayout content page"""
    implements(IContentPage)

    meta_type = "ContentPage"
    schema = ContentPageSchema

atapi.registerType(ContentPage, PROJECTNAME)
