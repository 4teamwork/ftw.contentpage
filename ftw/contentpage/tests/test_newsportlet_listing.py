from ftw.builder import Builder
from ftw.builder import create
from ftw.contentpage.portlets import news_portlet
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from unittest2 import TestCase
from zope.component import getMultiAdapter
from zope.component import getUtility



class TestNewsPortletListing(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.portal.REQUEST
        self.portal_url = self.portal.portal_url()

    def test_no_portlet_found(self):
        self.request.form.update({'portlet': 'not_existing'})
        view = self.portal.unrestrictedTraverse('news_portlet_listing')
        self.assertEqual(None, view.get_portlet())

    def test_portlet_found_in_leftcolumn(self):
        portlet = create(Builder('news portlet'))
        self.request.form.update({'portlet': portlet.__name__,
                                  'manager': u'plone.leftcolumn'})
        view = self.portal.unrestrictedTraverse('news_portlet_listing')
        self.assertEqual(portlet,
                         view.get_portlet().data)

    @browsing
    def test_leftcolumn_portlet(self, browser):
        folder = create(Builder('news folder').titled('News'))
        create(Builder('news').titled('Bookings open').within(folder))

        create(Builder('news portlet')
               .having(only_context=False,
                       path=['/{0}'.format(folder.getId())],
                       more_news_link=True))

        browser.login().open()
        browser.find('More News').click()
        self.assertEquals(['Bookings open'],
                          browser.css('h2.tileHeadline').text)

    @browsing
    def test_rightcolumn_portlet(self, browser):
        folder = create(Builder('news folder').titled('News'))
        create(Builder('news').titled('Bookings open').within(folder))

        create(Builder('news portlet')
               .in_manager(u'plone.rightcolumn')
               .having(only_context=False,
                       path=['/{0}'.format(folder.getId())],
                       more_news_link=True))

        browser.login().open()
        browser.find('More News').click()
        self.assertEquals(['Bookings open'],
                          browser.css('h2.tileHeadline').text)
