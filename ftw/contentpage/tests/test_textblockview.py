from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from unittest2 import TestCase
from simplelayout.base.interfaces import ISimpleLayoutBlock
from plone.testing.z2 import Browser
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
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

    def _create_textblock(self):
        textblock = self.contentpage.get(
            self.contentpage.invokeFactory('TextBlock', 'textblock'))
        # Fire all necessary events
        textblock.processForm()
        textblock.reindexObject()
        transaction.commit()
        return textblock

    def test_fti(self):
        self.assertIn('TextBlock', self.portal.portal_types.objectIds())

    def test_creation(self):
        _id = self.contentpage.invokeFactory('TextBlock', 'textblock')
        self.assertIn(_id, self.contentpage.objectIds())

    def test_simplelayout_integration(self):
        textblock = self._create_textblock()
        ISimpleLayoutBlock.providedBy(textblock)

    def test_addressblock_view(self):
        textblock = self._create_textblock()
        self._auth()
        self.browser.open(self.contentpage.absolute_url())
        self.assertIn(textblock.getId(), self.browser.contents)
        self.assertIn('simplelayout-block-wrapper TextBlock',
                      self.browser.contents)

    def tearDown(self):
        super(TestAddressBlockCreation, self).tearDown()
        portal = self.layer['portal']
        portal.manage_delObjects(['contentpage'])

        transaction.commit()
