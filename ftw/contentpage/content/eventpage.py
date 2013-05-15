from AccessControl import ClassSecurityInfo
from ftw.calendarwidget.browser.widgets import FtwCalendarWidget
from ftw.contentpage import _
from ftw.contentpage.config import PROJECTNAME
from ftw.contentpage.content.contentpage import ContentPage
from ftw.contentpage.content.contentpage import ContentPageSchema
from ftw.contentpage.content.textblock import image_schema
from ftw.contentpage.interfaces import IEventPage
from Products.Archetypes import atapi
from Products.ATContentTypes.config import HAS_LINGUA_PLONE
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from zope.interface import implements


if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import registerType
else:
    from Products.Archetypes.atapi import registerType


EventSchema = ContentPageSchema.copy() + atapi.Schema((
    atapi.DateTimeField(
        'startDate',
        required=True,
        searchable=False,
        accessor='start',
        languageIndependent=True,
        widget=FtwCalendarWidget(
            helper_js=('++resource++ftw.contentpage.resources/start_end_date_helper.js',),
            label=_(u'label_event_start', default=u'Event Starts'),
            description=_(u'help_start',
                          default=u"Date and Time, when the event begins."),
        ),
    ),

    atapi.DateTimeField(
        'endDate',
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

    atapi.BooleanField(
        'wholeDay',
        default=False,
        languageIndependent=True,
        widget=atapi.BooleanWidget(
            label=_(u'label_whole_day_event', u'Whole day event'),
            description=_(u'help_whole_day', default=u"Event lasts whole day"),
        ),
    ),
    atapi.StringField(
        'location',
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

# Protect the teaser image with a specific permission
permission = "ftw.contentpage: Edit teaser image on EventPage"
for name in image_schema.keys():
    EventSchema[name].write_permission = permission


class EventPage(ContentPage):
    implements(IEventPage)

    meta_type = "EventPage"
    schema = EventSchema
    security = ClassSecurityInfo()

    security.declarePublic('show_description')
    def show_description(self):
        return False


registerType(EventPage, PROJECTNAME)
