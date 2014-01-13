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


class IAuthoritySupport(Interface):
    """Marker interface for authorities"""


class IAuthority(Interface):
    """Marker interface for listing checkbox"""


class ICategorizable(Interface):
    """Marker interface for categorizable content"""


class INews(Interface):
    """Marker interface for news type"""


class INewsFolder(Interface):
    """Marker interface for newsfolder type"""


class IEventPage(Interface):
    """Marker interface for Event Type"""


class IEventFolder(Interface):
    """Marker interface for Event Type"""


class ITeaser(Interface):
    """Markter interface for the teaser functionality"""


class INewsListingView(Interface):
    """Marker interface for the news listing view"""


class IEventListingView(Interface):
    """Marker interface for the news listing view"""


class ISummaryListingEnabled(Interface):
    """Marker interface for the detail content listing view"""


class IFtwContentPageLayer(Interface):
    """Request marker for ftw.contentpage"""
