from Products.ATContentTypes.content import folder
from AccessControl import ClassSecurityInfo
from ftw.contentpage.config import PROJECTNAME
from simplelayout.base.interfaces import ISimpleLayoutCapable
from zope.interface import implements
from ftw.contentpage.interfaces import IEventFolder
from Products.Archetypes.atapi import registerType


class EventFolder(folder.ATFolder):

    implements(IEventFolder, ISimpleLayoutCapable)
    security = ClassSecurityInfo()


registerType(EventFolder, PROJECTNAME)
