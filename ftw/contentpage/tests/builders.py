from ftw.builder import builder_registry
from ftw.builder.archetypes import ArchetypesBuilder


class ContentPageBuilder(ArchetypesBuilder):

    portal_type = 'ContentPage'


builder_registry.register('content page', ContentPageBuilder)
