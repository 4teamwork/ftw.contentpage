from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from unittest2 import TestCase
from simplelayout.base.interfaces import ISimpleLayoutBlock
from plone.testing.z2 import Browser
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from plone.registry import Record, field
import transaction


class TestAddressBlockCreation(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestAddressBlockCreation, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

        self.contentpage = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'contentpage'))
        # Fire all necessary events
        self.contentpage.processForm()
        self.contentpage.reindexObject()
        transaction.commit()

        # Browser setup
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD, ))

    def _create_addressblock(self):
        addressblock = self.contentpage.get(
            self.contentpage.invokeFactory('AddressBlock', 'addressblock'))
        # Fire all necessary events
        addressblock.processForm()
        addressblock.reindexObject()
        transaction.commit()
        return addressblock

    def test_fti(self):
        self.assertIn('AddressBlock', self.portal.portal_types.objectIds())

    def test_creation(self):
        _id = self.contentpage.invokeFactory('AddressBlock', 'addressblock')
        self.assertIn(_id, self.contentpage.objectIds())

    def test_simplelayout_integration(self):
        addressblock = self.portal.get(
            self.contentpage.invokeFactory('AddressBlock', 'addressblock'))
        ISimpleLayoutBlock.providedBy(addressblock)

    def test_addressblock_view(self):
        addressblock = self._create_addressblock()
        self._auth()
        self.browser.open(self.contentpage.absolute_url())
        self.assertIn(addressblock.getId(), self.browser.contents)
        self.assertIn('simplelayout-block-wrapper AddressBlock',
                      self.browser.contents)

    def test_addressblock_default_title(self):
        addressblock = self._create_addressblock()
        self.assertEquals('Address', addressblock.Title())

        self._auth()
        self.browser.open(self.contentpage.absolute_url())
        self.assertIn('<h2>Address', self.browser.contents)

    def test_addressblock_change_default_title(self):
        registry = getUtility(IRegistry)
        registry.records['ftw.contentpage.addressblock.defaulttitle'] = \
            Record(field.TextLine(title=u"dummy", default=u"N/A"),
                   value=u'MyAddress')
        transaction.commit()

        addressblock = self._create_addressblock()
        self.assertEquals('MyAddress', addressblock.Title())

        self._auth()
        self.browser.open(self.contentpage.absolute_url())
        self.assertIn('<h2>MyAddress', self.browser.contents)

    def test_addressblock_change_title(self):
        addressblock = self._create_addressblock()
        addressblock.setTitle('New Title')
        transaction.commit()

        self._auth()
        self.browser.open(self.contentpage.absolute_url())
        self.assertIn('New Title', self.browser.contents)

    def test_default_country(self):
        addressblock = self._create_addressblock()
        self.assertEquals('Switzerland', addressblock.getCountry())

    def test_change_default_country(self):
        registry = getUtility(IRegistry)
        registry.records['ftw.contentpage.addressblock.defaultcountry'] = \
            Record(field.TextLine(title=u"dummy", default=u"N/A"),
                   value=u'Lichtenstein')
        transaction.commit()
        addressblock = self._create_addressblock()
        self.assertEquals('Lichtenstein', addressblock.getCountry())

    def test_exclude_from_nav(self):
        addressblock = self._create_addressblock()
        self.assertTrue(addressblock.getExcludeFromNav())

        self._auth()

    def test_display_opening_houers(self):
        addressblock = self._create_addressblock()
        addressblock.setOpeningHours("Monday to Friday")
        transaction.commit()

        self._auth()
        self.browser.open(self.contentpage.absolute_url())
        self.assertNotIn('<h2>Opening Hours', self.browser.contents)

        addressblock.setShowOpeningHours(True)
        transaction.commit()
        self.browser.open(self.contentpage.absolute_url())
        self.assertIn('<h2>Opening Hours', self.browser.contents)
        self.assertIn('Monday to Friday', self.browser.contents)

    def tearDown(self):
        super(TestAddressBlockCreation, self).tearDown()
        portal = self.layer['portal']
        portal.manage_delObjects(['contentpage'])

        registry = getUtility(IRegistry)
        registry.records['ftw.contentpage.addressblock.defaultcountry'] = \
            Record(field.TextLine(title=u"dummy", default=u"N/A"),
                   value=u'Switzerland')

        transaction.commit()
