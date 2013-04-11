from DateTime import DateTime
from AccessControl import ClassSecurityInfo
from ftw.contentpage.config import PROJECTNAME
from zope.interface import implements
from ftw.contentpage.interfaces import INews
from ftw.contentpage.content import contentpage
from Products.ATContentTypes.config import HAS_LINGUA_PLONE
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import registerType
else:
    from Products.Archetypes.atapi import registerType


news_schema = contentpage.ContentPageSchema.copy()

news_schema['effectiveDate'].required = True
news_schema['effectiveDate'].default_method = 'getDefaultEffectiveDate'
news_schema.changeSchemataForField('effectiveDate', 'default')
news_schema.changeSchemataForField('expirationDate', 'default')
news_schema.moveField('image', after='description')


class News(contentpage.ContentPage):

    implements(INews)
    security = ClassSecurityInfo()

    schema = news_schema

    def getDefaultEffectiveDate(self):
        return DateTime().Date()


registerType(News, PROJECTNAME)
