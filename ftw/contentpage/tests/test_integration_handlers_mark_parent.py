from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from unittest2 import TestCase
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from ftw.contentpage.interfaces import IOrgUnitMarker
from Products.CMFCore.utils import getToolByName
import transaction

# XXX: Currently I'm not able to test the catalog data
# In case of noLongerProvides and reindexObject the object_provides
# index has still the wrong values stored. If I test the same usecase
# with a real browser it works without any problems.


class TestOrgunitMarker(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestOrgunitMarker, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()
        self.catalog = getToolByName(self.portal, 'portal_catalog')

        self.contentpage = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'contentpage'))
        # Fire all necessary events
        self.contentpage.processForm()

        self.contentpage2 = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'contentpage2'))
        self.contentpage2.processForm()

        transaction.commit()

        # Browser setup
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD, ))

    def test_add_addressblock(self):
        addressblock = self.contentpage.get(
            self.contentpage.invokeFactory('AddressBlock', 'addressblock'))
        addressblock.processForm()
        self.assertTrue(IOrgUnitMarker.providedBy(self.contentpage))
        self.assertTrue(self.catalog(
            {'object_procvides': IOrgUnitMarker.__identifier__}))

    def test_add_addressblock_createobject(self):
        # CreateObject triggers diffrent events than invokefactory
        self._auth()
        self.browser.open("%s/createObject?type_name=AddressBlock" %
            self.contentpage.absolute_url())
        self.browser.getControl('Save').click()

        self.assertTrue(IOrgUnitMarker.providedBy(self.contentpage))
        self.assertTrue(self.catalog(
            {'object_procvides': IOrgUnitMarker.__identifier__}))

    def test_remove_addressblock(self):
        addressblock = self.contentpage.get(
            self.contentpage.invokeFactory('AddressBlock', 'addressblock'))
        addressblock.processForm()

        self.contentpage.manage_delObjects([addressblock.getId()])
        transaction.savepoint(optimistic=True)
        # self._auth()
        # self.browser.open(
        #     addressblock.absolute_url() + '/delete_confirmation')
        # self.browser.getControl("Delete").click()

        self.assertFalse(IOrgUnitMarker.providedBy(self.contentpage))

        # This works if we start up zope and do everything manually
        # self.assertFalse(self.catalog(
        #     {'UID': self.contentpage.UID(),
        #      'object_procvides': IOrgUnitMarker.__identifier__}))

    def test_add_multible_addressblocks(self):
        addressblock = self.contentpage.get(
            self.contentpage.invokeFactory('AddressBlock', 'addressblock'))
        addressblock.processForm()
        addressblock2 = self.contentpage.get(
            self.contentpage.invokeFactory('AddressBlock', 'addressblock2'))
        addressblock2.processForm()
        self.assertTrue(IOrgUnitMarker.providedBy(self.contentpage))

    def test_remove_multible_addressblocks(self):
        addressblock = self.contentpage.get(
            self.contentpage.invokeFactory('AddressBlock', 'addressblock'))
        addressblock.processForm()
        addressblock2 = self.contentpage.get(
            self.contentpage.invokeFactory('AddressBlock', 'addressblock2'))
        addressblock2.processForm()

        # Remove first addressblock
        self.contentpage.manage_delObjects([addressblock.getId()])
        self.assertTrue(IOrgUnitMarker.providedBy(self.contentpage))

        # Remove second addressblock
        self.contentpage.manage_delObjects([addressblock2.getId()])
        self.assertFalse(IOrgUnitMarker.providedBy(self.contentpage))

    def test_move_addressblock(self):
        addressblock = self.contentpage.get(
            self.contentpage.invokeFactory('AddressBlock', 'addressblock'))
        addressblock.processForm()
        transaction.savepoint(optimistic=True)
        # Cut and paste
        cutted = self.contentpage.manage_cutObjects([addressblock.getId()])
        transaction.commit()
        self.contentpage2.manage_pasteObjects(cutted)
        transaction.commit()

        self.assertNotIn('addressblock', self.contentpage.objectIds())
        self.assertFalse(IOrgUnitMarker.providedBy(self.contentpage))

        self.assertIn('addressblock', self.contentpage2.objectIds())
        self.assertTrue(IOrgUnitMarker.providedBy(self.contentpage2))

    def test_copy_addressblock(self):
        addressblock = self.contentpage.get(
            self.contentpage.invokeFactory('AddressBlock', 'addressblock'))
        addressblock.processForm()
        transaction.savepoint(optimistic=True)
        # Copy and paste
        cutted = self.contentpage.manage_copyObjects([addressblock.getId()])
        transaction.commit()
        self.contentpage2.manage_pasteObjects(cutted)
        transaction.commit()

        self.assertIn('addressblock', self.contentpage.objectIds())
        self.assertTrue(IOrgUnitMarker.providedBy(self.contentpage))

        self.assertIn('addressblock', self.contentpage2.objectIds())
        self.assertTrue(IOrgUnitMarker.providedBy(self.contentpage2))

    def tearDown(self):
        super(TestOrgunitMarker, self).tearDown()
        portal = self.layer['portal']
        portal.manage_delObjects(['contentpage', 'contentpage2'])
        transaction.commit()
