from AccessControl import ClassSecurityInfo
from ftw.contentpage import _
from ftw.contentpage import config
from ftw.contentpage.interfaces import IAddressBlock
from ftw.geo.interfaces import IGeocodableLocation
from plone.registry.interfaces import IRegistry
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from simplelayout.base.interfaces import ISimpleLayoutBlock
from simplelayout.types.common.content.simplelayout_schemas import \
    finalize_simplelayout_schema
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
        widget=atapi.StringWidget(
            label=_(u'label_addressTitle',
                    default=u'Address Title'))),

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
                default='Please enter a website URL'))),

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
        default_output_type='text/html',
        allowable_content_types=('text/html',),
        widget=atapi.TextAreaWidget(
            label=_(u'label_openingHours',
                    default=u'Opening Hours'),
            description=_(u'help_openingHours',
                          default=u''))),

    atapi.TextField(
        name='directions',
        schemata='default',
        default_output_type='text/html',
        allowable_content_types=('text/html',),
        widget=atapi.TextAreaWidget(
            label=_(u'label_directions',
                    default=u'Directions'),
            description=_(u'help_directions',
                          default=u''))),

))


addressblock_schema = ATContentTypeSchema.copy() + schema.copy()

addressblock_schema['excludeFromNav'].default = True
addressblock_schema['excludeFromNav'].visible = -1
addressblock_schema['title'].required = False
addressblock_schema['title'].default_method = 'getDefaultTitle'

finalize_simplelayout_schema(addressblock_schema)

addressblock_schema['description'].widget.visible = {'edit': 0, 'view': 0}
addressblock_schema['excludeFromNav'].visible = -1


class AddressBlock(ATCTContent, HistoryAwareMixin):

    security = ClassSecurityInfo()
    implements(IAddressBlock, ISimpleLayoutBlock, IGeocodableLocation)
    schema = addressblock_schema

    security.declarePrivate('getDefaultCountry')
    def getDefaultCountry(self):
        """ Returns the default country defined in registry.
        """
        registry = getUtility(IRegistry)
        return registry.get('ftw.contentpage.addressblock.defaultcountry',
                            'Switzerland')

    security.declarePrivate('getDefaultTitle')
    def getDefaultTitle(self):
        return translate(_(u'label_default_address',
                 default=u'Address'))

atapi.registerType(AddressBlock, config.PROJECTNAME)
