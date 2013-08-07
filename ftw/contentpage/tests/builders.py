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


class NewsBuilder(ArchetypesBuilder):

    portal_type = 'News'


builder_registry.register('news', NewsBuilder)
