from AccessControl import ClassSecurityInfo
from Acquisition import aq_parent
from borg.localrole.interfaces import IFactoryTempFolder
from ftw.contentpage import _
from ftw.contentpage import config
from ftw.contentpage.content.schema import finalize
from ftw.contentpage.interfaces import IAddressBlock
from ftw.geo.interfaces import IGeocodableLocation
from plone.registry.interfaces import IRegistry
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from simplelayout.base.interfaces import ISimpleLayoutBlock
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implements

from Products.ATContentTypes.config import HAS_LINGUA_PLONE
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone import public as atapi
else:
    from Products.Archetypes import atapi


schema = atapi.Schema((
    atapi.BooleanField(
        'showTitle',
        schemata='default',
        default=True,
        widget=atapi.BooleanWidget(
        label=_(u'label_show_title',
                default=u'Show Title'))),

    atapi.StringField(
        name='addressTitle',
        schemata='default',
        default_method='getDefaultAddressTitle',
        widget=atapi.StringWidget(
            label=_(u'label_addressTitle',
                    default=u'Address Title'))),

    atapi.StringField(
        name='department',
        schemata='default',
        widget=atapi.StringWidget(
            label=_(u'label_department',
                    default=u'Department'))),

    atapi.StringField(
        name='address',
        schemata='default',
        widget=atapi.StringWidget(
            label=_(u'label_address',
                    default=u'Address'))),

    atapi.StringField(
        name='extraAddressLine',
        schemata='default',
        widget=atapi.StringWidget(
            label=_(u'label_extraAddressLine',
                    default=u'Extra address line'))),

    atapi.StringField(
        name='zip',
        schemata='default',
        widget=atapi.StringWidget(
            label=_(u'label_zip',
                    default=u'ZIP'))),

    atapi.StringField(
        name='city',
        schemata='default',
        widget=atapi.StringWidget(
            label=_(u'label_city',
                    default=u'City'))),

    atapi.StringField(
        name='country',
        schemata='default',
        default_method='getDefaultCountry',
        widget=atapi.StringWidget(
            label=_(u'label_country',
                    default=u'Country'))),

    atapi.StringField(
        name='phone',
        schemata='default',
        widget=atapi.StringWidget(
            label=_(u'label_phone',
                    default=u'Phone'),
            description=_(u'help_phone',
                          default=u''))),

    atapi.StringField(
        name='fax',
        schemata='default',
        widget=atapi.StringWidget(
            label=_(u'label_fax',
                    default=u'Fax'),
            description=_(u'help_fax',
                          default=u''))),

    atapi.StringField(
        name='email',
        schemata='default',
        widget=atapi.StringWidget(
            label=_(u'label_email',
                    default=u'Email'))),

    atapi.StringField(
        'www',
        schemata='default',
        validators=('isURL',),
        widget=atapi.StringWidget(
            label=_(u'label_www', default='WWW'),
            description=_(
                u'help_www',
                default='Please enter a website URL (include http://, https://, etc)'))),

    atapi.BooleanField(
        name='showOpeningHours',
        schemata='default',
        widget=atapi.BooleanWidget(
            label=_(u'label_showOpeningHours',
                    default=u'Show opening hours'),
            description=_(u'help_showOpeningHours',
                          default=u''))),

    atapi.TextField(
        name='openingHours',
        schemata='default',
        default_input_type='text/html',
        default_output_type='text/x-html-safe',
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        widget=atapi.RichWidget(
            label=_(u'label_openingHours',
                    default=u'Opening Hours'),
            description=_(u'help_openingHours',
                          default=u''),
            allow_file_upload=False,
            rows=10)),

    atapi.TextField(
        name='directions',
        schemata='default',
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_input_type='text/html',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            label=_(u'label_directions',
                    default=u'Directions'),
            description=_(u'help_directions',
                          default=u''),
            allow_file_upload=False,
            rows=10)),
))


addressblock_schema = ATContentTypeSchema.copy() + schema.copy()

addressblock_schema['title'].required = False
addressblock_schema['title'].default_method = 'getDefaultTitle'

allowed_buttons = ('bold', 'link', 'unlink', 'anchor')

addressblock_schema['directions'].widget.allow_buttons = allowed_buttons
addressblock_schema['openingHours'].widget.allow_buttons = allowed_buttons

# Finalize schema
finalize(addressblock_schema, hide=['description'])


class AddressBlock(ATCTContent, HistoryAwareMixin):

    security = ClassSecurityInfo()
    implements(IAddressBlock, ISimpleLayoutBlock, IGeocodableLocation)
    schema = addressblock_schema

    security.declarePrivate('getDefaultCountry')
    def getDefaultCountry(self):
        """ Returns the default country defined in registry.
        """
        registry = getUtility(IRegistry)
        return translate(
            registry.get('ftw.contentpage.addressblock.defaultcountry',
                            ''),
            domain='ftw.contentpage',
            context=self.REQUEST)

    security.declarePrivate('getDefaultTitle')
    def getDefaultTitle(self):
        registry = getUtility(IRegistry)

        return translate(
            registry.get('ftw.contentpage.addressblock.defaulttitle', ''),
            domain='ftw.contentpage',
            context=self.REQUEST)

    security.declarePrivate('getDefaultAddressTitle')
    def getDefaultAddressTitle(self):
        parent = aq_parent(self)
        if IFactoryTempFolder.providedBy(parent):
            parent = aq_parent(aq_parent(parent))
        return parent.Title()

atapi.registerType(AddressBlock, config.PROJECTNAME)
