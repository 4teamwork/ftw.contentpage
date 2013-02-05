import unittest2 as unittest
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
import transaction
from simplelayout.base.interfaces import ISimpleLayoutCapable
from plone.testing.z2 import Browser
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
from StringIO import StringIO
import os

class TestNews(unittest.TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.newsfolder = self.portal.get(self.portal.invokeFactory('NewsFolder', 'newsfolder'))
        transaction.commit()
        self.browser = Browser(self.layer['app'])

    def test_creation_without_img(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))
        self.browser.open(self.newsfolder.absolute_url()+'/createObject?type_name=News')
        self.browser.getControl(name="title").value = "My News"
        self.browser.getControl(name="form.button.save").click()
        self.assertEqual(self.browser.url, 'http://nohost/plone/newsfolder/my-news/view')

    def test_creation_with_img(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))
        self.browser.open(self.newsfolder.absolute_url()+'/createObject?type_name=News')
        self.browser.getControl(name="title").value = "My News"
        file_ = open("%s/dummy.png" % os.path.split(__file__)[0])
        file_field = self.browser.getControl(name="image_file")
        file_field.add_file(StringIO(file_.read()), 'image/png', 'dummy.png')
        self.browser.getControl(name="form.button.save").click()
        self.assertIn('sl-img-wrapper', self.browser.contents)

    def test_interfaces(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))
        self.browser.open(self.newsfolder.absolute_url()+'/createObject?type_name=News')
        self.browser.getControl(name="title").value = "My News"
        self.browser.getControl(name="form.button.save").click()
        news = self.newsfolder.get("my-news")
        self.assertTrue(ISimpleLayoutCapable.providedBy(news))
