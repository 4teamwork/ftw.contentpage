from ftw.contentpage.testing import FTW_CONTENTPAGE_INTEGRATION_TESTING
from unittest2 import TestCase


class TestICSExport(TestCase):

    layer = FTW_CONTENTPAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.eventfolder = self.portal.get(self.portal.invokeFactory(
            'EventFolder', 'eventfolder'))
        self.eventfolder.processForm()

    def test_standard_export(self):
        kwargs = {'startDate': '2013-11-1 08:00',
                  'endDate': '2013-11-1 10:00',
                  'title': 'Event'}
        self.event = self.eventfolder.get(
            self.eventfolder.invokeFactory('EventPage', 'eventpage', **kwargs))

        address_args = {'address': 'Fakestreet 123',
                        'zip': '1234',
                        'city': 'mycity'}
        self.addressblock = self.event.get(
            self.event.invokeFactory('AddressBlock',
                                     'addresse',
                                     **address_args))

        view = self.event.restrictedTraverse('@@ics_view')
        view()
        result = view.feeddata()
        result_list = result.split('\n')

        expected = ['DTSTART:20131101T070000Z',
                    'DTEND:20131101T090000Z',
                    'LOCATION:Fakestreet 123\, 1234 mycity']
        self.assertTrue(set(expected).issubset(set(result_list)))

    def test_wholeday_export(self):
        kwargs = {'startDate': '2013-11-1',
                  'endDate': '2013-11-1',
                  'title': 'Event',
                  'wholeDay': True}
        self.event = self.eventfolder.get(
            self.eventfolder.invokeFactory('EventPage', 'eventpage', **kwargs))

        address_args = {'address': 'Fakestreet 123',
                        'zip': '1234',
                        'city': 'mycity'}
        self.addressblock = self.event.get(
            self.event.invokeFactory('AddressBlock',
                                     'addresse',
                                     **address_args))
        view = self.event.restrictedTraverse('@@ics_view')
        view()
        result = view.feeddata()
        result_list = result.split('\n')

        expected = ['DTSTART:20131031T230000Z',
                    'DTEND:20131031T230000Z',
                    'LOCATION:Fakestreet 123\, 1234 mycity']
        self.assertTrue(set(expected).issubset(set(result_list)))

    def test_multiday_export(self):
        kwargs = {'startDate': '2013-11-1',
                  'endDate': '2013-11-2',
                  'title': 'Event',
                  'wholeDay': True}
        self.event = self.eventfolder.get(
            self.eventfolder.invokeFactory('EventPage', 'eventpage', **kwargs))

        address_args = {'address': 'Fakestreet 123',
                        'zip': '1234',
                        'city': 'mycity'}
        self.addressblock = self.event.get(
            self.event.invokeFactory('AddressBlock',
                                     'addresse',
                                     **address_args))

        view = self.event.restrictedTraverse('@@ics_view')
        view()
        result = view.feeddata()
        result_list = result.split('\n')

        expected = ['DTSTART:20131031T230000Z',
                    'DTEND:20131101T230000Z',
                    'LOCATION:Fakestreet 123\, 1234 mycity']
        self.assertTrue(set(expected).issubset(set(result_list)))

    def test_export_without_addressblock(self):
        kwargs = {'startDate': '2013-11-1 08:00',
                  'endDate': '2013-11-1 10:00',
                  'title': 'Event',
                  'location': 'Towncentre'}
        self.event = self.eventfolder.get(
            self.eventfolder.invokeFactory('EventPage', 'eventpage', **kwargs))

        view = self.event.restrictedTraverse('@@ics_view')
        view()
        result = view.feeddata()
        result_list = result.split('\n')

        expected = ['LOCATION:Towncentre']
        self.assertTrue(set(expected).issubset(set(result_list)))
