from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import plone
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase
import transaction


class TestNewsListing(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.portal.invokeFactory('NewsFolder', 'nf1')
        self.context = self.portal.nf1

        # Create user with local Contributor role
        mtool = getToolByName(self.portal, 'portal_membership', None)
        mtool.addMember('john', 'password', ['Member'], [])
        self.portal.manage_permission('Access inactive portal content',
                                      ['Contributor', 'Manager'],
                                      acquire=False)
        self.context.manage_setLocalRoles('john', ['Contributor'])

        # Create user without special roles
        mtool.addMember('jack', 'password', ['Member'], [])

        self.context.invokeFactory('News', 'n1')
        self.context.invokeFactory('News', 'n2', effectiveDate=DateTime()+1)
        self.context.n2.reindexObject()
        transaction.commit()
        self._set_allowAnonymousViewAbout_property(True)

    def login(self):
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))

    def _set_allowAnonymousViewAbout_property(self, value):
        site_props = getToolByName(self.context, 'portal_properties').site_properties
        site_props._updateProperty('allowAnonymousViewAbout', value)
        transaction.commit()

    def is_author_visible(self):
        self.browser.open(self.context.absolute_url())
        return '<span class="documentAuthor"' in self.browser.contents

    def test_logged_in_user_sees_author_when_allowAnonymousViewAbout(self):
        self.login()
        self.assertTrue(self.is_author_visible(),
                        'Logged in user should see author if allowAnonymousViewAbout is True.')

    def test_logged_in_user_sees_author_when_not_allowAnonymousViewAbout(self):
        self.login()
        self._set_allowAnonymousViewAbout_property(False)
        self.assertTrue(self.is_author_visible(),
                        'Logged in user should see author if allowAnonymousViewAbout is False.')

    def test_anonymous_user_sees_author_when_allowAnonymousViewAbout(self):
        self.assertTrue(self.is_author_visible(),
                        'Anonymous user should see author if allowAnonymousViewAbout is True.')

    def test_anonymous_user_dont_sees_author_when_not_allowAnonymousViewAbout(self):
        self._set_allowAnonymousViewAbout_property(False)
        self.assertFalse(self.is_author_visible(),
                         'Anonymous user should not see author if allowAnonymousViewAbout is False.')

    def test_inactive_news_is_visible_for_contributor(self):
        self.browser.addHeader('Authorization', 'Basic john:password')
        self.browser.open(self.context.absolute_url())
        self.assertIn('n2', self.browser.contents)

    def test_inactive_news_is_not_visible_for_regular_users(self):
        self.browser.addHeader('Authorization', 'Basic jack:password')
        self.browser.open(self.context.absolute_url())
        self.assertNotIn('n2', self.browser.contents)

    @browsing
    def test_title_of_news_listing(self, browser):
        page = create(Builder('content page').titled('Contentpage'))
        newsfolder = create(Builder('news folder').within(page).titled('News'))

        browser.login().visit(page, view='@@newslisting')
        self.assertEquals('Contentpage - News', plone.first_heading())

        browser.visit(newsfolder)
        self.assertEquals('News', plone.first_heading())
