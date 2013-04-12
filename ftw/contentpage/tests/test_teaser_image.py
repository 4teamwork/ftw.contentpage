from ftw.contentpage.interfaces import ITeaser
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from pyquery import PyQuery
from StringIO import StringIO
from unittest2 import TestCase
import transaction


class TestTeaserImage(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestTeaserImage, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()
        self.catalog = getToolByName(self.portal, 'portal_catalog')

        self.contentpage = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'contentpage'))
        # Fire all necessary events
        self.contentpage.processForm()

        # Regular old simplayout page
        self.page = self.portal.get(
            self.portal.invokeFactory('Page', 'page'))
        self.page.processForm()

        transaction.commit()

        # Browser setup
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD, ))

    def test_teaser_interface(self):
        self.assertTrue(ITeaser.providedBy(self.contentpage),
            'ContentPage should provide ITeaser interface')

        self.assertFalse(ITeaser.providedBy(self.page),
            'Old Page should not provide ITeaser interface')

    def test_not_show_teaser(self):
        # No image, no description - no teaser
        self._auth()
        self.browser.open(self.contentpage.absolute_url())
        pq = PyQuery(self.browser.contents)
        self.assertFalse(
            pq('.simplelayout-content.sl-teaser-content-listing'),
            'There should be no simplelayout teaser viewlet')

        self.browser.open(self.page.absolute_url())
        pq = PyQuery(self.browser.contents)
        self.assertFalse(
            pq('.simplelayout-content.sl-teaser-content-listing'),
            'There should be no simplelayout teaser viewlet on old '
            'simplelayout pages')

    def test_show_teaser__description(self):
        self.contentpage.setDescription('qwerty')
        self.page.setDescription('qwerty')

        transaction.commit()

        self._auth()
        self.browser.open(self.contentpage.absolute_url())
        pq = PyQuery(self.browser.contents)

        wrapper = pq('.simplelayout-content.sl-teaser-content-listing')
        self.assertTrue(
            wrapper,
            'There should be the teaser viewlet')
        self.assertEquals(
            wrapper.find('.sl-text-wrapper')[0].text, 'qwerty')

        self.assertEquals(len(pq('.documentDescription')), 1,
            'The default description should appear only once')

        self.browser.open(self.page.absolute_url())
        pq = PyQuery(self.browser.contents)

        self.assertFalse(
            pq('.simplelayout-content.sl-teaser-content-listing'),
            'There should be still no simplelayout teaser viewlet on old '
            'simplelayout pages')

    def test_show_teaser__image(self):
        self.contentpage.setImage(
            StringIO('GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00'
                '\x00!\xf9\x04\x04\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00'
                '\x01\x00\x00\x02\x02D\x01\x00;'))

        self.assertNotIn('image', self.page.Schema(),
            'There should be no image field on old simplelayout pages')

        transaction.commit()

        self._auth()
        self.browser.open(self.contentpage.absolute_url())
        pq = PyQuery(self.browser.contents)

        wrapper = pq('.simplelayout-content.sl-teaser-content-listing')
        self.assertTrue(
            wrapper,
            'There should be the teaser viewlet')
        self.assertTrue(
            wrapper.find('.sl-img-wrapper'), 'No image found')

        self.browser.open(self.page.absolute_url())
        pq = PyQuery(self.browser.contents)

        self.assertFalse(
            pq('.simplelayout-content.sl-teaser-content-listing'),
            'There should be still no simplelayout teaser viewlet on old '
            'simplelayout pages')

    def test_teaser_field_permission(self):
        self._auth()
        self.browser.open("%s/edit" % self.contentpage.absolute_url())
        pq = PyQuery(self.browser.contents)
        self.assertTrue(pq('#fieldset-image .ArchetypesImageWidget'),
            'Expect an image field (teaser)')

        permissions = 'ftw.contentpage: Edit teaser image on ContentPage'
        self.contentpage.manage_permission(permissions, roles=[],
            acquire=False)
        self.contentpage.reindexObjectSecurity()
        transaction.commit()

        self.browser.open("%s/edit" % self.contentpage.absolute_url())
        pq = PyQuery(self.browser.contents)
        self.assertFalse(pq('#fieldset-image .ArchetypesImageWidget'),
            'Expect NO an image field (teaser)')
