from ftw.builder import builder_registry
from ftw.builder.archetypes import ArchetypesBuilder
from ftw.builder.content import ATImageBuilder
from ftw.builder.portlets import PlonePortletBuilder
from ftw.contentpage.portlets import news_archive_portlet
from ftw.contentpage.portlets import news_portlet
from ftw.contentpage.portlets import event_archive
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.container.interfaces import INameChooser
from zope.interface import alsoProvides
import transaction


class ContentPageBuilder(ArchetypesBuilder):

    portal_type = 'ContentPage'

    def __init__(self, *args, **kwargs):
        super(ContentPageBuilder, self).__init__(*args, **kwargs)
        self._providing_interfaces = []

    def providing(self, *interfaces):
        self._providing_interfaces.extend(interfaces)
        return self

    def after_create(self, obj):
        if self._providing_interfaces:
            alsoProvides(obj, *self._providing_interfaces)
            obj.reindexObject(idxs=['object_provides'])
        return super(ContentPageBuilder, self).after_create(obj)


builder_registry.register('content page', ContentPageBuilder)


class NewsBuilder(ContentPageBuilder):

    portal_type = 'News'


builder_registry.register('news', NewsBuilder)


class NewsFolderBuilder(ArchetypesBuilder):

    portal_type = 'NewsFolder'


builder_registry.register('news folder', NewsFolderBuilder)


class EventPageBuilder(ContentPageBuilder):

    portal_type = 'EventPage'


builder_registry.register('event page', EventPageBuilder)


class EventFolderBuilder(ArchetypesBuilder):

    portal_type = 'EventFolder'


builder_registry.register('event folder', EventFolderBuilder)


class AddressBlockBuilder(ArchetypesBuilder):

    portal_type = 'AddressBlock'


builder_registry.register('address block', AddressBlockBuilder)


class ListingBlockBuilder(ArchetypesBuilder):

    portal_type = 'ListingBlock'


builder_registry.register('listing block', ListingBlockBuilder)


class TextBlockBuilder(ATImageBuilder):

    portal_type = 'TextBlock'

    def attach(self, file_):
        self.arguments['image'] = file_
        return self

builder_registry.register('text block', TextBlockBuilder)


class NewsPortletBuilder(object):

    assignment_class = news_portlet.Assignment

    def __init__(self, session):
        self.session = session
        self.container = getSite()
        self.manager_name = u'plone.leftcolumn'
        self.arguments = {}

    def within(self, container):
        self.container = container
        return self

    def in_manager(self, manager_name):
        self.manager_name = manager_name
        return self

    def having(self, **kwargs):
        self.arguments.update(kwargs)
        return self

    def create(self):
        self.before_create()
        manager, assignments = self.get_manager_and_assignments()
        portlet = self.create_portlet(assignments)
        self.after_create(manager, assignments, portlet)
        return portlet

    def create_portlet(self, assignments):
        portlet = self.assignment_class(**self.arguments)
        name = self.choose_name(assignments, portlet)
        portlet.__name__ = portlet
        assignments[name] = portlet
        return portlet

    def get_manager_and_assignments(self):
        portal = getSite()
        manager = getUtility(IPortletManager,
                             name=self.manager_name,
                             context=portal)
        assignments = getMultiAdapter((self.container, manager),
                                      IPortletAssignmentMapping,
                                      context=portal)
        return manager, assignments

    def choose_name(self, assignments, portlet):
        return INameChooser(assignments).chooseName(
            portlet.__class__.__name__, portlet)

    def before_create(self):
        pass

    def after_create(self, manager, assignments, portlet):
        if self.session.auto_commit:
            transaction.commit()

builder_registry.register('news portlet', NewsPortletBuilder)


class EventArchivePortletBuilder(PlonePortletBuilder):
    assignment_class = event_archive.Assignment

    def __init__(self, session):
        super(EventArchivePortletBuilder, self).__init__(session)
        self.manager_name = u'plone.rightcolumn'

builder_registry.register('event archive portlet', EventArchivePortletBuilder)


class NewsArchivePortletBuilder(PlonePortletBuilder):
    assignment_class = news_archive_portlet.Assignment

    def __init__(self, session):
        super(NewsArchivePortletBuilder, self).__init__(session)
        self.manager_name = u'plone.rightcolumn'

builder_registry.register('news archive portlet', NewsArchivePortletBuilder)
