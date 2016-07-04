from DateTime import DateTime
from ftw.contentpage.browser.baselisting import extend_query_by_date
from ftw.contentpage.testing import FTW_CONTENTPAGE_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID
import datetime
import os
import unittest2 as unittest


class TestExtendQueryByDate(unittest.TestCase):

    def test_extend_query_by_date(self):
        query = extend_query_by_date({}, '2012/12/01', 'effective')
        self.assertEquals(
            {'effective':
                {'query': (
                    DateTime('2012/12/01').earliestTime(),
                    DateTime('2012/12/31').latestTime()),
                    'range': 'minmax'}},
            query)

    def test_query_does_not_lose_informations_if_date_is_incorrect(self):
        query = extend_query_by_date(
            {'Title': 'James'}, 'not a date', 'effective')
        self.assertEquals(query, {'Title': 'James'})


class TestNewsViews(unittest.TestCase):

    layer = FTW_CONTENTPAGE_INTEGRATION_TESTING

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
        self.news4 = self.newsfolder.get(self.newsfolder.invokeFactory(
                'News', 'news4', title="News without effective date",
                effectiveDate=None))

    def test_news_listing_view_no_restriction(self):
        listing = self.newsfolder.restrictedTraverse("@@newslisting")
        self.assertEqual(len(listing.get_items()), 5)
        brain = listing.get_items()[0]
        self.assertEqual(brain.Title, 'My News')
        self.assertTrue(listing.has_img(brain))
        self.assertIn(
            '<img src="http://nohost/plone/newsfolder/news/@@images/',
            listing.get_img(brain))
        self.assertEqual('test_user_1_', listing.get_creator(brain))

    def test_get_creator_no_member(self):
        listing = self.newsfolder.restrictedTraverse("@@newslisting")
        self.news.setCreators(['dummy'])
        self.news.reindexObject()

        brain = listing.get_items()[0]
        self.assertEquals('dummy', listing.get_creator(brain))

    def test_get_creator_has_fullname(self):
        listing = self.newsfolder.restrictedTraverse("@@newslisting")
        member = self.portal.portal_membership.getMemberById(TEST_USER_ID)
        member.setProperties(fullname='Firstname Lastname')

        brain = listing.get_items()[0]
        self.assertEquals('Firstname Lastname', listing.get_creator(brain))

    def test_news_listing_on_portal(self):
        listing = self.portal.restrictedTraverse("@@newslisting")
        self.assertEqual(len(listing.get_items()), 5)
