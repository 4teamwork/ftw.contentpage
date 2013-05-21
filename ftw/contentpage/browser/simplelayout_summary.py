from simplelayout.base.views import SimpleLayoutView
from simplelayout.base.interfaces import ISimplelayoutView
from ftw.contentpage.interfaces import ISummaryListingEnabled
from zope.interface import implements


class SimpleLayoutSummaryView(SimpleLayoutView):

    implements(ISimplelayoutView, ISummaryListingEnabled)
