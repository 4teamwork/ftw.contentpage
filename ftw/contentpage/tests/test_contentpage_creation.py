from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from unittest2 import TestCase
from simplelayout.base.interfaces import ISimpleLayoutCapable
from simplelayout.base.interfaces import IAdditionalListingEnabled
from plone.testing.z2 import Browser
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
import transaction


class TestContentPageCreation(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestContentPageCreation, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

        # Browser setup
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

    def test_fti(self):
        self.assertIn('ContentPage', self.portal.portal_types.objectIds())

    def test_creation(self):
        _id = self.portal.invokeFactory('ContentPage', 'contentpage')
        self.assertIn(_id, self.portal.objectIds())

        self._auth()
        self.browser.open('%s/createObject?type_name=ContentPage' %
            self.portal_url)
        self.browser.getControl("Title").value = 'New ContentPage'
        self.browser.getControl("Save").click()
        self.assertIn("New ContentPage", self.browser.contents)

    def test_getavailablelayouts(self):
        contentpage = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'contentpage'))
        mid = 'authorities_view'
        self.assertIn((mid, mid), contentpage.getAvailableLayouts())

        subpage = contentpage.get(
            contentpage.invokeFactory('ContentPage', 'subpage'))

        # authorities_view should no be available, check comment on
        # ftw.contentpage.content.contentpage -> getAvailableLayouts
        self.assertNotIn((mid, mid), subpage.getAvailableLayouts())

    def test_simplelayout_integration(self):
        contentpage = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'contentpage'))
        ISimpleLayoutCapable.providedBy(contentpage)
        IAdditionalListingEnabled.providedBy(contentpage)

    def test_simplelayout_view(self):
        _id = self.portal.invokeFactory('ContentPage', 'contentpage')
        transaction.commit()
        self._auth()
        self.browser.open(self.portal_url + '/' + _id)
        self.assertIn('template-simplelayout', self.browser.contents)
        self.assertIn('simplelayout-content', self.browser.contents)

    def tearDown(self):
        super(TestContentPageCreation, self).tearDown()
        portal = self.layer['portal']
        if 'contentpage' in portal.objectIds():
            portal.manage_delObjects(['contentpage'])
