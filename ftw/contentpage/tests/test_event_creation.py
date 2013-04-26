from ftw.contentpage.browser.eventlisting import format_date
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
from plone.testing.z2 import Browser
import transaction
import unittest2 as unittest


class TestEvent(unittest.TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.eventfolder = self.portal.get(self.portal.invokeFactory(
            'EventFolder', 'eventfolder'))
        self.eventfolder.processForm()
        transaction.commit()
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def test_creation(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))
        self.browser.open("%s/createObject?type_name=EventPage" %
            self.eventfolder.absolute_url())
        self.browser.getControl(name='title').value = 'A Title'
        self.browser.getControl(name='endDate_minute').value = ['20']
        self.browser.getControl(name='endDate_hour').value = ['08']
        self.browser.getControl(name='endDate_day').value = ['20']
        self.browser.getControl(name='endDate_month').value = ['05']
        self.browser.getControl(name='endDate_year').value = ['2013']
        self.browser.getControl(name='startDate_minute').value = ['20']
        self.browser.getControl(name='startDate_hour').value = ['07']
        self.browser.getControl(name='startDate_day').value = ['20']
        self.browser.getControl(name='startDate_month').value = ['05']
        self.browser.getControl(name='startDate_year').value = ['2013']
        self.browser.getControl(name='location').value = 'D\xc3\xbcbendorf'
        self.browser.getControl(name='form.button.save').click()
        self.assertEqual(self.browser.url,
            'http://nohost/plone/eventfolder/a-title/')
        event = self.eventfolder.get('a-title')
        self.assertEqual(event.location.encode('utf-8'), 'D\xc3\xbcbendorf')
        self.assertEqual(
            format_date(event.start(), event.end(), event.getWholeDay()),
            '20.05.2013 07:20 - 08:20')
