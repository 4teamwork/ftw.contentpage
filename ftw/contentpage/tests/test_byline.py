import unittest2 as unittest
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
import os
import transaction
from plone.testing.z2 import Browser
from zope.viewlet.interfaces import IViewletManager
from Products.Five.browser import BrowserView
from zope.component import queryMultiAdapter
from Products.CMFCore.utils import getToolByName


class TestByline(unittest.TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING


    def setUp(self):
        self.portal = self.layer['portal']

        self.newsfolder = self.portal.get(self.portal.invokeFactory(
                'NewsFolder', 'newsfolder'))
        image_ = open("%s/dummy.png" % os.path.split(__file__)[0])

        self.news = self.newsfolder.get(self.newsfolder.invokeFactory(
                'News', 'news', title="My News", image=image_))
        transaction.commit()
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False


    def _get_viewlet(self):
        view = BrowserView(self.news, self.news.REQUEST)
        manager_name = 'plone.belowcontenttitle'
        manager = queryMultiAdapter(
            (self.news, self.news.REQUEST, view),
            IViewletManager,
            manager_name)
        self.failUnless(manager)
        # Set up viewlets
        manager.update()
        name = 'plone.belowcontenttitle.documentbyline'
        return [v for v in manager.viewlets if v.__name__ == name]

    def test_byline_noworkflow(self):
        viewlet = self._get_viewlet()
        self.assertEqual(viewlet[0].getWorkflowState(), None)

    def test_byline_wf(self):
        self.wf_tool = getToolByName(self.portal, 'portal_workflow')
        self.wf_tool.setDefaultChain('simple_publication_workflow')
        viewlet = self._get_viewlet()
        self.assertEqual(viewlet[0].getWorkflowState(), 'Private')

    def test_byline_onestateworkflow(self):
        viewlet = self._get_viewlet()
        self.wf_tool = getToolByName(self.portal, 'portal_workflow')
        self.wf_tool.setDefaultChain('one_state_workflow')
        self.assertEqual(viewlet[0].getWorkflowState(), 'Published')
