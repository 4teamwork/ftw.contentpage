from datetime import datetime
from ftw.builder import create
from ftw.builder import Builder
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from pytz import timezone as tz
from unittest2 import TestCase


class TestNewsEffective(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.newsfolder = create(Builder('news folder'))

    def test_effective(self):
        self.news = create(Builder('news').within(self.newsfolder))
        difference = datetime.now(tz('Europe/Zurich')) -\
            self.news.effective().asdatetime()
        # The folllowing Calculation is the same as timedelta.total_seconds()
        # but since it isn't available in python2.6 we need to calculate it ourself
        # https://docs.python.org/2/library/datetime.html#datetime.timedelta.total_seconds
        self.assertLess((difference.microseconds +
                        (difference.seconds + difference.days * 24 * 3600)
                        * 10 ** 6) / 10.0 ** 6, 60)
