from AccessControl import ClassSecurityInfo
from ftw.contentpage.config import PROJECTNAME
from ftw.contentpage.interfaces import IEventFolder
from Products.ATContentTypes.config import HAS_LINGUA_PLONE
from Products.ATContentTypes.content import folder
from simplelayout.base.interfaces import ISimpleLayoutCapable
from zope.interface import implements


if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import registerType
else:
    from Products.Archetypes.atapi import registerType


class EventFolder(folder.ATFolder):

    implements(IEventFolder, ISimpleLayoutCapable)
    security = ClassSecurityInfo()


registerType(EventFolder, PROJECTNAME)
