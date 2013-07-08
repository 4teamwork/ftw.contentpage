from DateTime import DateTime
from ftw.contentpage.browser.newslisting import NewsListing
from ftw.contentpage.portlets.news_archive_portlet import Assignment
from ftw.contentpage.portlets.news_archive_portlet import Renderer
from ftw.contentpage.portlets.news_portlet import Assignment as NewsAssignment
from ftw.contentpage.portlets.news_portlet import Renderer as NewsRenderer
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
from plone.portlets.interfaces import IPortletManager
from plone.testing.z2 import Browser
from Products.CMFCore.TypesTool import FactoryTypeInformation
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from pyquery import PyQuery
from zope.component import getUtility
import os
import transaction
import unittest2 as unittest


class TestNewsPortlets(unittest.TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def _create_portlet(self):
        self.browser.open(
            self.portal.absolute_url() +
            '/++contextportlets++plone.leftcolumn/+/newsportlet'
            )
        self.browser.getControl(
            name="form.widgets.portlet_title").value = u"My Portlet"

        self.browser.getControl(name="form.buttons.add").click()

    def setUp(self):
        self.portal = self.layer['portal']
        self.browser = Browser(self.layer['portal'])
        self.browser.handleErrors = False
        self.newsfolder1 = self.portal.get(self.portal.invokeFactory(
                'NewsFolder', 'newsfolder1', title="Newsfolder1"))
        self.newsfolder2 = self.portal.get(self.portal.invokeFactory(
                'NewsFolder', 'newsfolder2', title="Newsfolder2"))
        self.newsfolder1.invokeFactory(
            'News',
            'news1',
            description="This Description must be longer than 50 chars"
            " so we are able to test if it will be croped",
            image=open("%s/dummy.png" % os.path.split(__file__)[0], 'r'),
            effectiveDate=DateTime() - 1)  # Yesterday
        self.newsfolder1.invokeFactory(
            'News', 'news2',
            effectiveDate=DateTime() - 15)  # Few days ago
        self.newsfolder2.invokeFactory(
            'News', 'news3',
            effectiveDate=DateTime() - 100)  # Old News
        self.newsfolder2.invokeFactory(
            'News', 'news4',
            effectiveDate=DateTime() + 5)  # Further news
        transaction.commit()
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

    def test_area_path_validator(self):
        self.browser.open(
            self.portal.absolute_url() +
            '/++contextportlets++plone.leftcolumn/+/newsportlet'
            )
        self.browser.getControl(
            name="form.widgets.portlet_title").value = u"My Portlet"
        #Get Control over the Query Field and enter a value.
        self.browser.getControl(
            name="form.widgets.path.widgets.query").value = u"ne"
        #Click the Searchbutton
        self.browser.getControl(
            name="form.widgets.path.buttons.search").click()
        # select the correct radio button over the Label.
        #Remember to use the Text of the Label and not the id. It won't work.
        self.browser.getControl("Newsfolder1").selected = True

        self.browser.getControl("label_only_context").selected = True
        self.browser.getControl(name="form.buttons.add").click()

        self.assertIn('You can not set a path and limit to context.',
                      self.browser.contents)

    def test_create_portlet_only_context(self):
        self.browser.open(
            self.portal.absolute_url() +
            '/++contextportlets++plone.leftcolumn/+/newsportlet'
            )
        self.browser.getControl(
            name="form.widgets.portlet_title").value = u"My Portlet"

        self.browser.getControl(name="form.buttons.add").click()
        self.browser.open(self.portal.absolute_url())

        self.assertIn('newsfolder1/news1', self.browser.contents)
        self.assertIn('newsfolder1/news2', self.browser.contents)
        self.assertIn('newsfolder2/news3', self.browser.contents)
        self.assertIn('newsfolder2/news4', self.browser.contents)
        self.browser.open(self.portal.newsfolder1.absolute_url())
        self.assertIn('newsfolder1/news1', self.browser.contents)
        self.assertIn('newsfolder1/news2', self.browser.contents)
        self.assertFalse('newsfolder2/news3' in self.browser.contents)
        self.assertFalse('newsfolder2/news4' in self.browser.contents)

    def test_create_portlet_path(self):
        self.browser.open(
            self.portal.absolute_url() +
            '/++contextportlets++plone.leftcolumn/+/newsportlet'
            )
        self.browser.getControl(
            name="form.widgets.portlet_title").value = u"My Portlet"
        #Get Control over the Query Field and enter a value.
        self.browser.getControl(
            name="form.widgets.path.widgets.query").value = u"ne"
        #Click the Searchbutton
        self.browser.getControl(
            name="form.widgets.path.buttons.search").click()
        # select the correct radio button over the Label.
        #Remember to use the Text of the Label and not the id. It won't work.
        self.browser.getControl("Newsfolder1").selected = True

        self.browser.getControl("label_only_context").selected = False
        self.browser.getControl(name="form.buttons.add").click()
        self.browser.open(self.portal.newsfolder1.absolute_url())
        self.assertIn('newsfolder1/news1', self.browser.contents)
        self.assertIn('newsfolder1/news2', self.browser.contents)
        self.assertFalse('newsfolder2/news3' in self.browser.contents)
        self.assertFalse('newsfolder2/news4' in self.browser.contents)

    def test_create_portlet_no_img(self):
        self.browser.open(
            self.portal.absolute_url() +
            '/++contextportlets++plone.leftcolumn/+/newsportlet'
            )
        self.browser.getControl(
            name="form.widgets.portlet_title").value = u"My Portlet"
        #Get Control over the Query Field and enter a value.
        self.browser.getControl(
            name="form.widgets.path.widgets.query").value = u"ne"
        #Click the Searchbutton
        self.browser.getControl(
            name="form.widgets.path.buttons.search").click()
        # select the correct radio button over the Label.
        #Remember to use the Text of the Label and not the id. It won't work.
        self.browser.getControl("Newsfolder1").selected = True
        self.browser.getControl("label_show_image").selected = False

        self.browser.getControl("label_only_context").selected = False
        self.browser.getControl(name="form.buttons.add").click()
        self.browser.open(self.portal.newsfolder1.absolute_url())
        self.assertNotIn('<div class="newsImage"', self.browser.contents)

    def test_create_portlet_crop_desc(self):
        self._create_portlet()
        self.browser.open(self.portal.absolute_url())
        self.assertIn('This Description must be longer than 50 chars so ...',
                      self.browser.contents)

    def test_create_portlet_desc_off(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

        self.browser.open(
            self.portal.absolute_url() +
            '/++contextportlets++plone.leftcolumn/+/newsportlet')
        self.browser.getControl(
            name="form.widgets.portlet_title").value = u"My Portlet"
        #Get Control over the Query Field and enter a value.
        self.browser.getControl(
            name="form.widgets.path.widgets.query").value = u"ne"
        #Click the Searchbutton
        self.browser.getControl(
            name="form.widgets.path.buttons.search").click()
        # select the correct radio button over the Label.
        #Remember to use the Text of the Label and not the id. It won't work.
        self.browser.getControl(
            "Newsfolder1").selected = True

        self.browser.getControl("Show Description").selected = False
        self.browser.getControl(name="form.buttons.add").click()
        self.browser.open(self.portal.absolute_url())
        self.assertFalse('This Description' in self.browser.contents)

    def test_no_classificationItems(self):
        self.browser.open(
            self.portal.absolute_url() +
            '/++contextportlets++plone.leftcolumn/+/newsportlet')
        self.assertNotIn('<div class="contenttreeWidget"'
                         'id="form-widgets-classification_items-contenttree">',
                         self.browser.contents
                         )

    def test_classificationItems(self):
        types_tool = getToolByName(self.portal, 'portal_types')
        types_tool['ClassificationItem'] = FactoryTypeInformation(
            'ClassificationItem')
        transaction.commit()
        self.browser.open(
            self.portal.absolute_url() +
            '/++contextportlets++plone.leftcolumn/+/newsportlet'
            )
        self.assertIn('<div class="contenttreeWidget"'
                      ' id="form-widgets-classification_items-contenttree">',
                      self.browser.contents
                      )

    def test_editform_empty(self):
        self._create_portlet()
        self.browser.getLink("News Portlet").click()
        self.browser.getControl(name="form.buttons.apply").click()
        self.assertEqual(
                self.portal.absolute_url() + '/@@manage-portlets',
                self.browser.url
                )

    def test_editform_cancel(self):
        self._create_portlet()
        self.browser.getLink("News Portlet").click()
        self.browser.getControl(
                name="form.widgets.portlet_title").value = u"Not My Portlet"
        self.browser.getControl(
                name="form.buttons.cancel_add").click()
        self.assertEqual(
                self.portal.absolute_url() + '/@@manage-portlets',
                self.browser.url
                )
        self.browser.getLink("News Portlet").click()
        self.assertNotEqual(
                self.browser.getControl(
                    name="form.widgets.portlet_title").value,
                "Not My Portlet"
                )

    def test_editform_success(self):
        self._create_portlet()
        self.browser.getLink("News Portlet").click()
        self.browser.getControl(
                name="form.widgets.portlet_title").value = u"My edited Portlet"
        self.browser.getControl(name="form.buttons.apply").click()
        self.assertEqual(self.portal.absolute_url() + '/@@manage-portlets',
                         self.browser.url)
        self.browser.getLink("News Portlet").click()
        self.assertEqual(
                self.browser.getControl(
                    name="form.widgets.portlet_title").value,
                "My edited Portlet"
                )

    def test_editform_send_error(self):
        self._create_portlet()
        self.browser.getLink("News Portlet").click()
        self.browser.getControl(name="form.widgets.portlet_title").value = u""
        self.browser.getControl(name="form.buttons.apply").click()
        self.assertIn('<div class="error">Required input is missing.</div>',
                      self.browser.contents)

    def test_image_viewlet(self):
        self._create_portlet()
        self.browser.open(self.portal.absolute_url())
        self.assertIn('<div class="newsImage">'
                      '<img src="http://nohost/plone/'
                      'newsfolder1/news1/@@images/',
                      self.browser.contents)

    def test_addform_cancel(self):
        self.browser.open(
                self.portal.absolute_url() +
                '/++contextportlets++plone.leftcolumn/+/newsportlet'
                )
        self.browser.getControl(name="form.buttons.cancel_add").click()
        self.assertEqual(self.portal.absolute_url() + '/@@manage-portlets',
                         self.browser.url)

    def test_addform_send_error(self):
        self.browser.open(
                self.portal.absolute_url() +
                '/++contextportlets++plone.leftcolumn/+/newsportlet'
                )
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

        self.browser.open(
                self.portal.absolute_url() +
                '/++contextportlets++plone.leftcolumn/+/newsportlet')
        #Get Control over the Query Field and enter a value.
        self.browser.getControl(
                name="form.widgets.path.widgets.query").value = u"ne"
        #Click the Searchbutton
        self.browser.getControl(
                name="form.widgets.path.buttons.search").click()
        self.browser.getControl("Newsfolder1").selected = True

        self.browser.getControl("label_only_context").selected = False
        self.browser.getControl(name="form.buttons.add").click()
        self.assertIn('<div class="error">Required input is missing.</div>',
                      self.browser.contents)

    def test_days_no_filter(self):
        context = self.portal
        portlet = NewsAssignment(days=0, only_context=False)
        manager = getUtility(IPortletManager, name=u"plone.leftcolumn")
        renderer = NewsRenderer(context, context.REQUEST, BrowserView,
                                manager, portlet)
        self.assertEquals(len(renderer.get_news()), 4, 'Expect all 4 news')

    def test_days_filter(self):
        context = self.portal
        portlet = NewsAssignment(days=5, only_context=False)
        manager = getUtility(IPortletManager, name=u"plone.leftcolumn")
        renderer = NewsRenderer(context, context.REQUEST, BrowserView,
                                manager, portlet)

        self.assertEquals(len(renderer.get_news()), 2, 'Expect 2 news')

        portlet = NewsAssignment(days=28, only_context=False)
        renderer = NewsRenderer(context, context.REQUEST, BrowserView,
                                manager, portlet)
        self.assertEquals(len(renderer.get_news()), 3, 'Expect 3 news')

    def test_archive_portlet_empty(self):
        # Separate test for the archive portlet, because we need static dates
        archivefolder = self.portal.get(self.portal.invokeFactory(
                'NewsFolder', 'archivefolder', title="Archive Test"))

        manager = getUtility(IPortletManager, name=u"plone.leftcolumn")
        portlet = Assignment()
        view = NewsListing(archivefolder, archivefolder.REQUEST)
        renderer = Renderer(archivefolder, archivefolder.REQUEST, view,
                            manager, portlet)

        self.assertFalse(renderer.available,
                         'Did no expect an archive portlet')

    def test_archive_portlet(self):
        manager = getUtility(IPortletManager, name=u"plone.leftcolumn")

        archivefolder = self.portal.get(self.portal.invokeFactory(
                'NewsFolder', 'archivefolder', title="Archive Test"))

        archivefolder.invokeFactory(
            'News', 'news1', effectiveDate=DateTime('2013/01/20'))
        archivefolder.invokeFactory(
            'News', 'news2',
            effectiveDate=DateTime('2013/01/21'))
        archivefolder.invokeFactory(
            'News', 'news3', effectiveDate=DateTime('2012/12/20'))
        archivefolder.invokeFactory(
            'News', 'news4', effectiveDate=DateTime('2012/12/21'))
        archivefolder.invokeFactory(
            'News', 'news5', effectiveDate=None)

        portlet = Assignment()
        view = NewsListing(archivefolder, archivefolder.REQUEST)
        renderer = Renderer(archivefolder, archivefolder.REQUEST, view,
                            manager, portlet)

        self.assertTrue(renderer.available,
                        'There should be an archive portlet')

        self.assertEquals(
            [{'mark': False,
              'months': [{'mark': False,
                          'number': 2,
                          'title': u'January',
                          'url': 'http://nohost/plone/archivefolder/'
                                  'news_listing?archive=2013/01/01'}],
              'number': 2,
              'title': '2013'},
             {'mark': False,
              'months': [{'mark': False,
                          'number': 2,
                          'title': u'December',
                          'url': 'http://nohost/plone/archivefolder/'
                                  'news_listing?archive=2012/12/01'}],
              'number': 2,
              'title': '2012'}],
              renderer.archive_summary())

    def test_archive_portlets_is_available_on_newslisting(self):
        manager = getUtility(IPortletManager, name=u"plone.leftcolumn")
        portlet = Assignment()
        view = NewsListing(self.portal, self.portal.REQUEST)
        renderer = Renderer(self.portal, self.portal.REQUEST, view,
                            manager, portlet)

        self.assertTrue(renderer.available,
            'News Archive portlet should be available on NewsListing View')

    def test_news_archive_portlet(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD, ))

        self.browser.open(
            '%s/++contextportlets++plone.leftcolumn/+/newsarchiveportlet' %
            self.newsfolder1.absolute_url())

        self.browser.open(self.newsfolder1.absolute_url())

        pq = PyQuery(self.browser.contents)
        self.assertTrue(pq('.portlet.portletArchiveListing'),
            'We added one, so there sould be a EventArchive portlet')

        self.assertGreater(
            len(pq('.portlet.portletArchiveListing .portletItem li')), 0,
            'Expect at least one entry in the events archive portlet')

    def test_newsportlet_more_news_link_disabled(self):
        manager = getUtility(IPortletManager, name=u"plone.leftcolumn")
        portlet = NewsAssignment()
        renderer = NewsRenderer(self.portal, self.portal.REQUEST, object(),
                            manager, portlet)

        self.assertFalse(renderer.show_more_news_link(),
            'Expect that the "More News" link is invisible')

    def test_newsportlet_more_news_link_enabled(self):
        manager = getUtility(IPortletManager, name=u"plone.leftcolumn")
        portlet = NewsAssignment(more_news_link=True)
        renderer = NewsRenderer(self.portal, self.portal.REQUEST, object(),
                            manager, portlet)

        self.assertTrue(renderer.show_more_news_link(),
            'Expect that the "More News" link is visible')
