import unittest2 as unittest
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
import transaction
from plone.testing.z2 import Browser
import os


class TestNewsViews(unittest.TestCase):

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

    def test_news_listing_view(self):
        listing = self.newsfolder.restrictedTraverse("@@news_listing")
        brain = listing.get_news()[0]
        self.assertEqual(brain.Title, 'My News')
        self.assertTrue(listing.has_img(brain))
        self.assertIn(
            '<img src="http://nohost/plone/newsfolder/news/@@images/',
            listing.get_img(brain)
            )
        self.assertEqual(listing.get_creator(brain).id, 'test_user_1_')
