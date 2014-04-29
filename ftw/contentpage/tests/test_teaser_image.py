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

    def test_not_show_teaser(self):
        # No image, no description - no teaser
        self._auth()
        self.browser.open(self.contentpage.absolute_url())
        pq = PyQuery(self.browser.contents)
        self.assertFalse(
            pq('.simplelayout-content.sl-teaser-content-listing'),
            'There should be no simplelayout teaser viewlet')

    def test_show_teaser__description(self):
        self.contentpage.setDescription('qwerty')

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

    def test_show_teaser__image(self):
        self.contentpage.setImage(
            StringIO('GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00'
                '\x00!\xf9\x04\x04\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00'
                '\x01\x00\x00\x02\x02D\x01\x00;'))

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

    def test_teaser_field_permission_contentpage(self):
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

    def test_teaser_field_permission_eventpage(self):
        eventfolder = self.portal.get(self.portal.invokeFactory(
            'EventFolder', 'eventfolder'))
        eventfolder.processForm()

        eventpage = eventfolder.get(
            eventfolder.invokeFactory('EventPage', 'eventpage'))
        eventpage.processForm()
        transaction.commit()

        self._auth()
        self.browser.open("%s/edit" % eventpage.absolute_url())
        pq = PyQuery(self.browser.contents)
        self.assertTrue(pq('#fieldset-image .ArchetypesImageWidget'),
            'Expect an image field (teaser)')

        permissions = 'ftw.contentpage: Edit teaser image on EventPage'
        eventpage.manage_permission(permissions, roles=[],
            acquire=False)
        eventpage.reindexObjectSecurity()
        transaction.commit()

        self.browser.open("%s/edit" % eventpage.absolute_url())
        pq = PyQuery(self.browser.contents)
        self.assertFalse(pq('#fieldset-image .ArchetypesImageWidget'),
            'Expect NO an image field (teaser)')

    def test_teaser_field_permission_news(self):
        newsfolder = self.portal.get(self.portal.invokeFactory(
            'NewsFolder', 'newsfolder'))
        newsfolder.processForm()

        news = newsfolder.get(
            newsfolder.invokeFactory('News', 'news'))
        news.processForm()
        transaction.commit()

        self._auth()
        self.browser.open("%s/edit" % news.absolute_url())
        pq = PyQuery(self.browser.contents)
        self.assertTrue(pq('#fieldset-image .ArchetypesImageWidget'),
            'Expect an image field (teaser)')

        permissions = 'ftw.contentpage: Edit teaser image on News'
        news.manage_permission(permissions, roles=[],
            acquire=False)
        news.reindexObjectSecurity()
        transaction.commit()

        self.browser.open("%s/edit" % news.absolute_url())
        pq = PyQuery(self.browser.contents)
        self.assertFalse(pq('#fieldset-image .ArchetypesImageWidget'),
            'Expect NO an image field (teaser)')

    def test_teaser_viewlet_not_used_when_not_on_a_simplelayout_view(self):
        self.contentpage.setDescription('The Description')
        transaction.commit()
        self._auth()

        self.browser.open(self.contentpage.absolute_url())
        self.assertTrue(
            self.teaser_viewlet_visible(),
            'Expected the teaser viewlet to be visible on a normal content page.')

        self.browser.open('/'.join((self.contentpage.absolute_url(),
                                    'folder_contents')))
        self.assertFalse(
            self.teaser_viewlet_visible(),
            'Unexpectedly found traces of the teaser viewlet on folder_contents.')

    def teaser_viewlet_visible(self):
        pq = PyQuery(self.browser.contents)
        return pq('.sl-teaser-content-listing')
