from ftw.geo.interfaces import IGeocodableLocation
from zope.component import adapts
from zope.interface import implements
from ftw.contentpage.interfaces import IAddressBlock


class AddressBlockLocationAdapter(object):
    """Adapter that is able to represent the location of an MyType in
    a geocodable string form.
    """
    implements(IGeocodableLocation)
    adapts(IAddressBlock)

    def __init__(self, context):
        self.context = context

    def getLocationString(self):
        """Build a geocodable location string from the AddressBlocks address
        related fields.
        """
        street = self.context.getAddress().strip()
        # Remove Postfach form street, otherwise Google geocoder API will
        # return wrong results
        street = street.replace('Postfach', '').replace('\r', '').strip()
        zip_code = self.context.getZip()
        city = self.context.getCity()
        country = self.context.getCountry()

        location = ', '.join([street, zip_code, city, country])

        # We need at least something other than country to be defined,
        # otherwise we shouldn't try to do a geocode lookup
        if not (street or zip_code or city):
            return ''

        return location
