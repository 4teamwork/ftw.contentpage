from ftw.builder import builder_registry
from ftw.builder.archetypes import ArchetypesBuilder
from zope.interface import alsoProvides


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


class TextBlockBuilder(ArchetypesBuilder):

    portal_type = 'TextBlock'


builder_registry.register('text block', TextBlockBuilder)
