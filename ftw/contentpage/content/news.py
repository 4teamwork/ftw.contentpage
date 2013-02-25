from DateTime import DateTime
from AccessControl import ClassSecurityInfo
from ftw.contentpage.config import PROJECTNAME
from zope.interface import implements
from ftw.contentpage.interfaces import INews
from Products.ATContentTypes.content import folder
from simplelayout.base.interfaces import ISimpleLayoutCapable
from ftw.contentpage.content.textblock import image_schema
from Products.ATContentTypes.config import HAS_LINGUA_PLONE
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import registerType
else:
    from Products.Archetypes.atapi import registerType


news_schema = folder.ATFolderSchema.copy() + image_schema.copy()

news_schema['effectiveDate'].required = True
news_schema['effectiveDate'].default_method = 'getDefaultEffectiveDate'
news_schema.changeSchemataForField('effectiveDate', 'default')
news_schema.changeSchemataForField('expirationDate', 'default')
news_schema.moveField('image', after='description')


class News(folder.ATFolder):

    implements(INews, ISimpleLayoutCapable)
    security = ClassSecurityInfo()

    schema = news_schema

    def getDefaultEffectiveDate(self):
        return DateTime().Date()

    security.declarePublic('showAddMenu')
    def showAddMenu(self):
        return False

    security.declarePublic('show_description')
    def show_description(self):
        return False


registerType(News, PROJECTNAME)
