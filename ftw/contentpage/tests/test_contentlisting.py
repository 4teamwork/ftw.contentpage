from ftw.contentpage import config
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from simplelayout.base.views import SimpleLayoutView
from unittest2 import TestCase
from zope.viewlet.interfaces import IViewletManager


from zope.component import queryMultiAdapter
import transaction


class TestContentListing(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestContentListing, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

        self.contentpage = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'contentpage'))
        # Fire all necessary events
        self.contentpage.processForm()
        transaction.commit()

        # Browser setup
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD, ))

    def _get_viewlet(self):
        view = SimpleLayoutView(self.contentpage, self.contentpage.REQUEST)
        manager_name = 'simplelayout.base.listing'
        manager = queryMultiAdapter(
            (self.contentpage, self.contentpage.REQUEST, view),
            IViewletManager,
            manager_name)
        self.failUnless(manager)
        # Set up viewlets
        manager.update()
        name = 'ftw.contentpage.contentlisting'
        return [v for v in manager.viewlets if v.__name__ == name]

    def test_component_registered(self):
        self.assertTrue(len(self._get_viewlet()) == 1)

    def test_category_field(self):
        self.assertIn('categories', self.contentpage.Schema())
        self.contentpage.Schema()['categories'].set(self.contentpage, 'DEMO1')
        self.assertEquals(
            self.contentpage.Schema()['categories'].get(self.contentpage),
            ('DEMO1',))

    def test_category_index(self):
        catalog = getToolByName(self.portal, 'portal_catalog')
        for name, meta_type in config.INDEXES:
            self.assertIn(name, catalog.indexes())

        subpage = self.contentpage.get(
            self.contentpage.invokeFactory('ContentPage', 'subpage'))
        subpage.processForm()
        subpage.setTitle('Subpage title')
        subpage.Schema()['categories'].set(subpage, 'DEMO1')
        subpage.reindexObject()
        self.assertTrue(catalog({'categories': 'DEMO1'})[0])

    def test_viewlet(self):
        viewlet = self._get_viewlet()[0]
        # Should be empty
        self.assertFalse(viewlet.available())
        # Create more content
        subpage = self.contentpage.get(
            self.contentpage.invokeFactory('ContentPage', 'subpage'))
        subpage.setTitle('Subpage')
        subpage.Schema()['categories'].set(subpage, 'DEMO1')
        subpage.reindexObject()
        subpage2 = self.contentpage.get(
            self.contentpage.invokeFactory('ContentPage', 'subpage2'))
        subpage2.setTitle('Subpage2')
        subpage2.Schema()['categories'].set(subpage2, 'DEMO2')
        subpage2.reindexObject()
        subpage3 = self.contentpage.get(
            self.contentpage.invokeFactory('ContentPage', 'subpage3'))
        subpage3.setTitle('Subpage3')
        subpage3.Schema()['categories'].set(subpage3, 'DEMO2')
        subpage3.reindexObject()

        viewlet = self._get_viewlet()[0]
        self.assertTrue(viewlet.available())
        self.assertEquals(viewlet.get_content(),
                          [('DEMO1', [('Subpage',
                                       subpage.absolute_url())]),
                           ('DEMO2', [('Subpage2',
                                       subpage2.absolute_url()),
                                      ('Subpage3',
                                       subpage3.absolute_url())])])
        transaction.commit()
        self._auth()
        self.browser.open(self.contentpage.absolute_url())
        self.assertIn('DEMO1', self.browser.contents)
        self.assertIn('DEMO2', self.browser.contents)
        self.assertIn('subelements-listing-element', self.browser.contents)


    def tearDown(self):
        super(TestContentListing, self).tearDown()
        portal = self.layer['portal']
        portal.manage_delObjects(['contentpage'])
        transaction.commit()
