from DateTime import DateTime
from ftw.contentpage.browser.eventlisting import format_date
import unittest2 as unittest


class TestEvent(unittest.TestCase):

    def test_same_date(self):
        start = DateTime(2013, 01, 01, 18, 00)
        end = DateTime(2013, 01, 01, 19, 00)
        wholeday = False

        self.assertEquals(format_date(start, end, wholeday),
            '01.01.2013 18:00 - 19:00')

    def test_diff_date(self):
        start = DateTime(2013, 01, 01, 18, 00)
        end = DateTime(2013, 01, 03, 19, 00)
        wholeday = False

        self.assertEquals(format_date(start, end, wholeday),
            '01.01.2013 18:00 - 03.01.2013 19:00')

    def test_same_date_wholeday(self):
        start = DateTime(2013, 01, 01)
        end = DateTime(2013, 01, 01)
        wholeday = True

        self.assertEquals(format_date(start, end, wholeday),
            '01.01.2013')

    def test_diff_date_wholeday(self):
        start = DateTime(2013, 01, 01)
        end = DateTime(2013, 01, 03)
        wholeday = True

        self.assertEquals(format_date(start, end, wholeday),
            '01.01.2013 - 03.01.2013')

    def test_same_data_same_time(self):
        start = DateTime(2013, 01, 01, 11, 00)
        end = DateTime(2013, 01, 01, 11, 00)
        wholeday = False

        self.assertEquals(format_date(start, end, wholeday),
            '01.01.2013 11:00')
