from AccessControl import ClassSecurityInfo
from ftw.contentpage import _
from ftw.contentpage import config
from ftw.contentpage.content.schema import finalize
from ftw.contentpage.interfaces import ITextBlock
from plone.app.blob.field import ImageField
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.CMFCore.utils import getToolByName
from simplelayout.base.interfaces import ISimpleLayoutBlock
from zope.interface import implements

from Products.ATContentTypes.config import HAS_LINGUA_PLONE
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone import public as atapi
else:
    from Products.Archetypes import atapi


default_schema = atapi.Schema((
    atapi.BooleanField(
        name='showTitle',
        schemata='default',
        default=0,
        widget=atapi.BooleanWidget(
        label=_(u'label_show_title',
                default=u'Show Title'))),

    atapi.TextField(
        name='text',
        required=False,
        searchable=True,
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_input_type='text/html',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            label=_(u'label_text',
                    default=u'Text'),
                    rows=25)),

))

image_schema = atapi.Schema((
    ImageField(
        name='image',
        required=False,
        original_size=config.ORIGINAL_SIZE,
        schemata='image',
        widget=atapi.ImageWidget(
            label=_(u'label_image',
                    default=u'Image'))),

    atapi.BooleanField(
        name='imageClickable',
        schemata='image',
        default=0,
        widget=atapi.BooleanWidget(
            label=_(u'label_image_clickable',
                    default=u'Image clickable'),
            description=_(u'description_image_clickable',
                          default=u'Opens image in an overlay'))),

    atapi.StringField(
        name='imageCaption',
        required=False,
        searchable=True,
        schemata='image',
        widget=atapi.StringWidget(
            label=_(u'label_image_caption',
                    default=u'Image'))),

    atapi.StringField(
            name='imageAltText',
            schemata='image',
            required=False,
            widget=atapi.StringWidget(
                label=_(u'label_image_alt_text',
                        default=u'Image'),
                description=_(u'description_image_alt_text',
                              default=u'Enter an alternative text '
                                      u'for the image'))),
))


textblock_schema = ATContentTypeSchema.copy() + \
    default_schema.copy() + image_schema.copy()

textblock_schema['title'].required = False
textblock_schema['description'].widget.visible = {'view': 'invisible',
                                                  'edit': 'invisible'}
textblock_schema['text'].widget.filter_buttons = ('image', )

finalize(textblock_schema)


class TextBlock(ATCTContent, HistoryAwareMixin):
    """Textblock for Contentpage
    """
    security = ClassSecurityInfo()
    implements(ITextBlock, ISimpleLayoutBlock)
    schema = textblock_schema

    #Special workarround for empty titles, otherwise we have "[...]"
    #results in the search function
    def setTitle(self, value):
        portal_transforms = getToolByName(self, 'portal_transforms')
        field = self.schema['title']
        if not value:
            new_value = self.REQUEST.get('text', None)
            if new_value is not None:
                converted = portal_transforms.convertTo(
                    'text/plain',
                    new_value).getData().replace('\r', '').replace('\n', '')
                crop = self.restrictedTraverse('@@plone').cropText
                cropped = crop(converted, 30, '')
                field.set(self, cropped.strip())
        else:
            field.set(self, value)

atapi.registerType(TextBlock, config.PROJECTNAME)
