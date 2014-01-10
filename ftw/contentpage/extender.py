from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from ftw.contentpage import _
from ftw.contentpage.interfaces import ICategorizable
from ftw.contentpage.interfaces import IListingMarker
from ftw.contentpage.interfaces import IShowListingMarkerCheckbox
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.public import KeywordWidget
from Products.Archetypes.public import LinesField
from zope.component import adapts
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import noLongerProvides


class CategoriesField(ExtensionField, LinesField):
    """A reference field to store object topic"""


class CategoriesExtender(object):
    adapts(ICategorizable)
    implements(IOrderableSchemaExtender)

    fields = [CategoriesField(
        'content_categories',
        multiValued=True,
        searchable=False,
        accessor='getContentCategories',
        roleBasedAdd=True,
        widget=KeywordWidget(
            label=_(u'label_categories', default=u'Categories'),
            description=_(u'help_categories',
                          default=u'Category for contentlisting'),
        ),
    ), ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, original):
        return original


class ListingMarkerCheckbox(ExtensionField, BooleanField):
    """ Listing marker checkbox field """

    def set(self, instance, value, **kwargs):
        """ Copied code from BooleanField, extended by set/unset the marker
        interface.
        """
        if not value or value == '0' or value == 'False':
            value = False
            noLongerProvides(instance, IListingMarker)
        else:
            alsoProvides(instance, IListingMarker)
            value = True

        self.getStorage(instance).set(self.getName(),
                instance, value, **kwargs)


class ListingMarkerExtender(object):
    adapts(IShowListingMarkerCheckbox)
    implements(IOrderableSchemaExtender)

    fields = [ListingMarkerCheckbox(
        'mark_for_listings',
        searchable=False,
        required=False,
        default=False,
        widget=BooleanWidget(
            label=_(u'label_mark_for_listings',
                    default=u'Mark content for listings'),
            description=_(u'help_mark_for_listings',
                          default=u'')))]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, original):
        return original
