import unittest2 as unittest
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
import transaction
from plone.testing.z2 import Browser
import os
import datetime

class TestNewsViews(unittest.TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        self.newsfolder = self.portal.get(self.portal.invokeFactory(
                'NewsFolder', 'newsfolder'))
        image_ = open("%s/dummy.png" % os.path.split(__file__)[0])

        self.news = self.newsfolder.get(self.newsfolder.invokeFactory(
                'News', 'news', title="My News", image=image_))
        self.news1 = self.newsfolder.get(self.newsfolder.invokeFactory(
                'News', 'news1', title="My News1", image=image_, effectiveDate=(datetime.datetime.now() - datetime.timedelta(7))))
        self.news2 = self.newsfolder.get(self.newsfolder.invokeFactory(
                'News', 'news2', title="My News2", image=image_, effectiveDate=(datetime.datetime.now() - datetime.timedelta(14))))
        self.news3 = self.newsfolder.get(self.newsfolder.invokeFactory(
                'News', 'news3', title="My News3", image=image_, effectiveDate=(datetime.datetime.now() - datetime.timedelta(21))))

        transaction.commit()
        self.browser = Browser(self.layer['app'])

    def test_news_listing_view_no_restriction(self):
        listing = self.newsfolder.restrictedTraverse("@@news_listing")
        self.assertEqual(len(listing.get_news()), 4)
        brain = listing.get_news()[0]
        self.assertEqual(brain.Title, 'My News')
        self.assertTrue(listing.has_img(brain))
        self.assertIn(
            '<img src="http://nohost/plone/newsfolder/news/@@images/',
            listing.get_img(brain)
            )
        self.assertEqual(listing.get_creator(brain).id, 'test_user_1_')

    def test_news_listing_start(self):
        date = datetime.datetime.now() - datetime.timedelta(15)
        self.newsfolder.REQUEST.form['start'] = date.strftime('%d.%m.%Y')
        listing = self.newsfolder.restrictedTraverse("@@news_listing")
        self.assertEqual(len(listing.get_news()), 3)

    def test_news_listing_end(self):
        date = datetime.datetime.now() - datetime.timedelta(10)
        self.newsfolder.REQUEST.form['end'] = date.strftime('%d.%m.%Y')
        listing = self.newsfolder.restrictedTraverse("@@news_listing")
        self.assertEqual(len(listing.get_news()), 2)

    def test_news_listing_start_and_end(self):
        end = datetime.datetime.now() - datetime.timedelta(10)
        start = datetime.datetime.now() - datetime.timedelta(15)
        self.newsfolder.REQUEST.form['end'] = end.strftime('%d.%m.%Y')
        self.newsfolder.REQUEST.form['start'] = start.strftime('%d.%m.%Y')
        listing = self.newsfolder.restrictedTraverse("@@news_listing")
        self.assertEqual(len(listing.get_news()), 1)
