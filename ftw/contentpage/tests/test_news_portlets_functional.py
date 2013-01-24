import unittest2 as unittest
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
import transaction
from plone.testing.z2 import Browser
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
import os
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.TypesTool import FactoryTypeInformation


class TestNewsPortlets(unittest.TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def _create_portlet(self):
        self.browser.open(self.portal.absolute_url()+'/++contextportlets++plone.leftcolumn/+/newsportlet')
        self.browser.getControl(name="form.widgets.portlet_title").value = u"My Portlet"
        #Get Control over the Query Field and enter a value.
        self.browser.getControl(name="form.widgets.path.widgets.query").value = u"ne"
        #Click the Searchbutton
        self.browser.getControl(name="form.widgets.path.buttons.search").click()
        # select the correct radio button over the Label. Remember to use the Text of the Label and not the id. It won't work.
        self.browser.getControl("Newsfolder1").selected = True


        self.browser.getControl(name="form.buttons.add").click()

    def setUp(self):
        self.portal = self.layer['portal']
        self.browser = Browser(self.layer['portal'])
        self.browser.handleErrors
        self.newsfolder1 = self.portal.get(self.portal.invokeFactory('NewsFolder', 'newsfolder1', title="Newsfolder1"))
        self.newsfolder2 = self.portal.get(self.portal.invokeFactory('NewsFolder', 'newsfolder2', title="Newsfolder2"))
        self.newsfolder1.invokeFactory('News', 'news1', description="This Description must be longer than 50 chars so we are able to test if it will be croped", image=open("%s/dummy.png" % os.path.split(__file__)[0], 'r'))
        self.newsfolder1.invokeFactory('News', 'news2')
        self.newsfolder2.invokeFactory('News', 'news3')
        self.newsfolder2.invokeFactory('News', 'news4')
        transaction.commit()

    def test_create_portlet_only_context(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

        self.browser.open(self.portal.absolute_url()+'/++contextportlets++plone.leftcolumn/+/newsportlet')
        self.browser.getControl(name="form.widgets.portlet_title").value = u"My Portlet"
        #Get Control over the Query Field and enter a value.
        self.browser.getControl(name="form.widgets.path.widgets.query").value = u"ne"
        #Click the Searchbutton

        self.browser.getControl(name="form.widgets.path.buttons.search").click()
        # select the correct radio button over the Label. Remember to use the Text of the Label and not the id. It won't work.
        self.browser.getControl("Newsfolder1").selected = True

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
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

        self.browser.open(self.portal.absolute_url()+'/++contextportlets++plone.leftcolumn/+/newsportlet')
        self.browser.getControl(name="form.widgets.portlet_title").value = u"My Portlet"
        #Get Control over the Query Field and enter a value.
        self.browser.getControl(name="form.widgets.path.widgets.query").value = u"ne"
        #Click the Searchbutton
        self.browser.getControl(name="form.widgets.path.buttons.search").click()
        # select the correct radio button over the Label. Remember to use the Text of the Label and not the id. It won't work.
        self.browser.getControl("Newsfolder1").selected = True


        self.browser.getControl("label_only_context").selected = False
        self.browser.getControl(name="form.buttons.add").click()
        self.browser.open(self.portal.newsfolder1.absolute_url())
        self.assertIn('newsfolder1/news1', self.browser.contents)
        self.assertIn('newsfolder1/news2', self.browser.contents)
        self.assertFalse('newsfolder2/news3' in self.browser.contents)
        self.assertFalse('newsfolder2/news4' in self.browser.contents)

    def test_create_portlet_crop_desc(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

        self._create_portlet()
        self.browser.open(self.portal.absolute_url())
        self.assertIn('This Description must be longer than 50 chars so ...', self.browser.contents)

    def test_create_portlet_desc_off(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

        self.browser.open(self.portal.absolute_url()+'/++contextportlets++plone.leftcolumn/+/newsportlet')
        self.browser.getControl(name="form.widgets.portlet_title").value = u"My Portlet"
        #Get Control over the Query Field and enter a value.
        self.browser.getControl(name="form.widgets.path.widgets.query").value = u"ne"
        #Click the Searchbutton
        self.browser.getControl(name="form.widgets.path.buttons.search").click()
        # select the correct radio button over the Label. Remember to use the Text of the Label and not the id. It won't work.
        self.browser.getControl("Newsfolder1").selected = True

        self.browser.getControl("Show Description").selected = False
        self.browser.getControl(name="form.buttons.add").click()
        self.browser.open(self.portal.absolute_url())
        self.assertFalse('This Description' in self.browser.contents)


    def test_no_classificationItems(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))
        self.browser.open(self.portal.absolute_url()+'/++contextportlets++plone.leftcolumn/+/newsportlet')
        self.assertNotIn('<div class="contenttreeWidget" id="form-widgets-classification_items-contenttree">', self.browser.contents)


    def test_classificationItems(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

        types_tool = getToolByName(self.portal, 'portal_types')
        types_tool['ClassificationItem'] = FactoryTypeInformation('ClassificationItem')
        transaction.commit()
        self.browser.open(self.portal.absolute_url()+'/++contextportlets++plone.leftcolumn/+/newsportlet')
        self.assertIn('<div class="contenttreeWidget" id="form-widgets-classification_items-contenttree">', self.browser.contents)
        #view = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn/+/newsportlet')
        #view()
        #import pdb; pdb.set_trace()

    def test_editform_empty(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))
        self._create_portlet()
        self.browser.getLink("News Portlet").click()
        self.browser.getControl(name="form.buttons.apply").click()
        self.assertEqual(self.portal.absolute_url()+'/@@manage-portlets', self.browser.url)

    def test_editform_cancel(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

        self._create_portlet()
        self.browser.getLink("News Portlet").click()
        self.browser.getControl(name="form.widgets.portlet_title").value = u"Not My Portlet"
        self.browser.getControl(name="form.buttons.cancel_add").click()
        self.assertEqual(self.portal.absolute_url()+'/@@manage-portlets', self.browser.url)
        self.browser.getLink("News Portlet").click()
        self.assertNotEqual(self.browser.getControl(name="form.widgets.portlet_title").value, "Not My Portlet")

    def test_editform_success(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

        self._create_portlet()
        self.browser.getLink("News Portlet").click()
        self.browser.getControl(name="form.widgets.portlet_title").value = u"My edited Portlet"
        self.browser.getControl(name="form.buttons.apply").click()
        self.assertEqual(self.portal.absolute_url()+'/@@manage-portlets', self.browser.url)
        self.browser.getLink("News Portlet").click()
        self.assertEqual(self.browser.getControl(name="form.widgets.portlet_title").value, "My edited Portlet")

    def test_editform_send_error(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

        self._create_portlet()
        self.browser.getLink("News Portlet").click()
        self.browser.getControl(name="form.widgets.portlet_title").value = u""
        self.browser.getControl(name="form.buttons.apply").click()
        self.assertIn('<div class="error">Required input is missing.</div>', self.browser.contents)

    def test_image_viewlet(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

        self._create_portlet()
        self.browser.open(self.portal.absolute_url())
        self.assertIn('<div class="newsImage"><img src="http://nohost/plone/newsfolder1/news1/@@images/', self.browser.contents)

    def test_addform_cancel(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

        self.browser.open(self.portal.absolute_url()+'/++contextportlets++plone.leftcolumn/+/newsportlet')
        self.browser.getControl(name="form.buttons.cancel_add").click()
        self.assertEqual(self.portal.absolute_url()+'/@@manage-portlets', self.browser.url)

    def test_addform_send_error(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

        self.browser.open(self.portal.absolute_url()+'/++contextportlets++plone.leftcolumn/+/newsportlet')
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

        self.browser.open(self.portal.absolute_url()+'/++contextportlets++plone.leftcolumn/+/newsportlet')
        #Get Control over the Query Field and enter a value.
        self.browser.getControl(name="form.widgets.path.widgets.query").value = u"ne"
        #Click the Searchbutton
        self.browser.getControl(name="form.widgets.path.buttons.search").click()
        # select the correct radio button over the Label. Remember to use the Text of the Label and not the id. It won't work.
        self.browser.getControl("Newsfolder1").selected = True


        self.browser.getControl("label_only_context").selected = False
        self.browser.getControl(name="form.buttons.add").click()
        self.assertIn('<div class="error">Required input is missing.</div>', self.browser.contents)
