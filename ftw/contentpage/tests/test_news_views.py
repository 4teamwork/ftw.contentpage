from DateTime import DateTime
from ftw.contentpage.browser.newslisting import extend_query_by_date
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from plone.testing.z2 import Browser
import datetime
import os
import transaction
import unittest2 as unittest


class TestExtendQueryByDate(unittest.TestCase):

    def test_extend_query_by_date(self):
        query = {}
        extend_query_by_date(query, '2012/12/01')
        self.assertEquals(query,
            {'effective':
                {'query': (DateTime('2012/12/01').earliestTime(),
                           DateTime('2012/12/31').latestTime()),
                 'range': 'minmax'}})

        extend_query_by_date(query, '2013/02/01')
        self.assertEquals(query,
            {'effective':
                {'query': (DateTime('2013/02/01').earliestTime(),
                           DateTime('2013/02/28').latestTime()),
                 'range': 'minmax'}})

        # fallback
        query = {}
        extend_query_by_date(query, 'not a date')
        self.assertEquals(query, {})


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
                'News', 'news1', title="My News1", image=image_,
                effectiveDate=(
                    datetime.datetime.now() - datetime.timedelta(7))))
        self.news2 = self.newsfolder.get(self.newsfolder.invokeFactory(
                'News', 'news2', title="My News2", image=image_,
                effectiveDate=(
                    datetime.datetime.now() - datetime.timedelta(14))))
        self.news3 = self.newsfolder.get(self.newsfolder.invokeFactory(
                'News', 'news3', title="My News3", image=image_,
                effectiveDate=(
                    datetime.datetime.now() - datetime.timedelta(21))))

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
        self.assertEqual(listing.get_creator(brain), 'test_user_1_')
