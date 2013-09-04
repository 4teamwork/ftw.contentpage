from AccessControl import ClassSecurityInfo
from ftw.contentpage.config import PROJECTNAME
from ftw.contentpage.interfaces import INewsFolder
from Products.ATContentTypes.config import HAS_LINGUA_PLONE
from Products.ATContentTypes.content import folder
from zope.interface import implements


if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import registerType
else:
    from Products.Archetypes.atapi import registerType


class NewsFolder(folder.ATFolder):

    implements(INewsFolder)
    security = ClassSecurityInfo()


registerType(NewsFolder, PROJECTNAME)
