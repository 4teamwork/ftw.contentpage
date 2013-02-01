from zope.interface import Interface


class IContentPage(Interface):
    """Marker interface for ContenPages"""


class IAddressBlock(Interface):
    """Marker interface for AddressBlocks"""


class IListingBlock(Interface):
    """Marker interface for AddressBlocks"""


class IAddressBlockView(Interface):
    """Marker interface for AddressBlocks"""


class ITextBlock(Interface):
    """Marker interface for TextBlocks"""


class IOrgUnitMarker(Interface):
    """Marker interface for AddressBlocks"""


class ICategorizable(Interface):
    """Marker interface for categorizable content"""


class INews(Interface):
    """Marker interface for news type"""


class INewsFolder(Interface):
    """Marker interface for newsfolder type"""
