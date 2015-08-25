from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from ftw.contentpage.config import PROJECTNAME
from ftw.contentpage.content import contentpage
from ftw.contentpage.content.textblock import image_schema
from ftw.contentpage.interfaces import INews
from Products.ATContentTypes.config import HAS_LINGUA_PLONE
from zope.interface import implements


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


# Protect the teaser image with a specific permission
permission = "ftw.contentpage: Edit teaser image on News"
for name in image_schema.keys():
    news_schema[name].write_permission = permission


class News(contentpage.ContentPage):

    implements(INews)
    security = ClassSecurityInfo()

    schema = news_schema

    def getDefaultEffectiveDate(self):
        return DateTime()


registerType(News, PROJECTNAME)
