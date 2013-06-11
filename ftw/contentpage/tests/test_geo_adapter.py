from ftw.testing import MockTestCase
from ftw.contentpage.testing import ZCML_LAYER
from ftw.contentpage.interfaces import IAddressBlock
from ftw.geo.interfaces import IGeocodableLocation
from zope.component import getGlobalSiteManager
from ftw.contentpage.geo import AddressBlockLocationAdapter


class TestGeoAdapter(MockTestCase):

    layer = ZCML_LAYER

    def setUp(self):
        super(TestGeoAdapter, self).setUp()

        self.context = self.providing_stub(IAddressBlock)

        gsm = getGlobalSiteManager()
        gsm.registerAdapter(AddressBlockLocationAdapter)

    def test_no_address_data(self):
        self.expect(self.context.getAddress()).result('')
        self.expect(self.context.getZip()).result('')
        self.expect(self.context.getCity()).result('')
        self.expect(self.context.getCountry()).result('')
        self.replay()

        adapter = IGeocodableLocation(self.context)
        self.assertEquals(adapter.getLocationString(), '')

    def test_address_data(self):
        self.expect(self.context.getAddress()).result('street')
        self.expect(self.context.getZip()).result('zip')
        self.expect(self.context.getCity()).result('city')
        self.expect(self.context.getCountry()).result('country')

        self.replay()

        adapter = IGeocodableLocation(self.context)

        self.assertEquals(adapter.getLocationString(),
                          'street, zip, city, country')
