from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from unittest2 import TestCase
from ftw.contentpage.portlets import news_portlet
from zope.component import getMultiAdapter
from zope.component import getUtility
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager



class TestNewsPortletListing(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.portal.REQUEST
        self.portal_url = self.portal.portal_url()

        leftColumn = getUtility(IPortletManager,
                                name=u'plone.leftcolumn',
                                context=self.portal)
        left = getMultiAdapter((self.portal, leftColumn,),
                               IPortletAssignmentMapping,
                               context=self.portal)
        self.news_assignment = news_portlet.Assignment()
        left[u'news'] = self.news_assignment

    def test_no_portlet_found(self):
        self.request.form.update({'portlet': 'not_existing'})
        view = self.portal.unrestrictedTraverse('news_portlet_listing')
        self.assertEqual(None, view.get_portlet())

    def test_portlet_found(self):
        self.request.form.update({'portlet': 'news'})
        view = self.portal.unrestrictedTraverse('news_portlet_listing')
        self.assertEqual(self.news_assignment,
                         view.get_portlet().data)
