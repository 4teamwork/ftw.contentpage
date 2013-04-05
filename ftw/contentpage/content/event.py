from ftw.contentpage.content.contentpage import ContentPage
from ftw.contentpage.content.contentpage import ContentPageSchema
from Products.Archetypes import atapi
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from ftw.calendarwidget.browser.widgets import FtwCalendarWidget
from ftw.contentpage import _
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from ftw.contentpage.interfaces import IEvent
from ftw.contentpage.config import PROJECTNAME
from Products.ATContentTypes.utils import DT2dt

EventSchema = ContentPageSchema.copy() + atapi.Schema((
    atapi.DateTimeField('startDate',
        required=True,
        searchable=False,
        accessor='start',
        languageIndependent=True,
        widget=FtwCalendarWidget(
            label=_(u'label_event_start', default=u'Event Starts'),
            description=_(u'help_start',
                          default=u"Date and Time, when the event begins."),
            ),
        ),

    atapi.DateTimeField('endDate',
        required=True,
        searchable=False,
        accessor='end',
        languageIndependent=True,
        widget=FtwCalendarWidget(
            label=_(u'label_event_end', default=u'Event Ends'),
            description=_(u'help_end',
                          default=u"Date and Time, when the event ends."),
            ),
        ),

    atapi.BooleanField('wholeDay',
        default=False,
        languageIndependent=True,
        widget=atapi.BooleanWidget(
            label=_(u'label_whole_day_event', u'Whole day event'),
            description=_(u'help_whole_day', default=u"Event lasts whole day"),
            ),
        ),
    atapi.StringField('location',
                      searchable=True,
                      widget=atapi.StringWidget(
                label=_(u'label_event_location', default=u'Event Location'),
                description=_(u'help_event_location', default=u""),
                ),
                ),

    ))

finalizeATCTSchema(EventSchema)
# finalizeATCTSchema moves 'location' into 'categories', we move it back:
EventSchema.changeSchemataForField('location', 'default')

class Event(ContentPage):
    implements(IEvent)

    meta_type = "Event"
    schema = EventSchema
    security = ClassSecurityInfo()

    def getDate(self):
        start = DT2dt(self.start())
        start_date = start.date().strftime('%d.%m.%Y')
        if not self.getWholeDay():
            start_time = start.time().strftime('%H:%M')
            end = DT2dt(self.end())
            end_date = end.date().strftime('%d.%m.%Y')
            end_time = end.time().strftime('%H:%M')
            if start_date == end_date:
                return start_date + ' ' + start_time + ' - ' + end_time
            else:
                return start_date + ' ' + start_time + ' - ' + end_date + ' ' + end_time
        else:
            return start_date

atapi.registerType(Event, PROJECTNAME)
