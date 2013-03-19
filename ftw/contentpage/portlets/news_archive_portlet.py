from DateTime import DateTime
from plone.app.portlets.portlets import base
from plone.memoize.view import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.i18nl10n import monthname_msgid
from Products.CMFPlone.utils import base_hasattr
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.i18n import translate
from zope.interface import implements


class INewsArchivePortlet(IPortletDataProvider):
    """Archive portlet interface.
"""


class Assignment(base.Assignment):
    implements(INewsArchivePortlet)

    @property
    def title(self):
        return "News Archive Portlet"


class Renderer(base.Renderer):

    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.data = data
        self.request = request

    @property
    def available(self):
        """Only show the portlet, if there are News
        """
        return bool(self.archive_summary())

    def zLocalizedTime(self, time, long_format=False):
        """Convert time to localized time
        """
        month_msgid = monthname_msgid(time.strftime("%m"))
        month = translate(month_msgid, domain='plonelocales',
                          context=self.request)

        return u"%s %s" % (month, time.strftime('%Y'))

    @memoize
    def archive_summary(self):
        """Returns an ordered list of summary infos per month."""
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {}
        if base_hasattr(self.context, 'getTranslations'):
            roots = self.context.getTranslations(
                review_state=False).values()
            root_path = ['/'.join(br.getPhysicalPath()) for br in roots]
            query['Language'] = 'all'
        else:
            root_path = '/'.join(self.context.getPhysicalPath())

        query['path'] = root_path
        query['portal_type'] = 'News'

        archive_counts = {}
        entries = catalog(**query)
        for entry in entries:
            year_month = entry.effective.strftime('%Y/%m')
            if year_month in archive_counts:
                archive_counts[year_month] += 1
            else:
                archive_counts[year_month] = 1

        archive_summary = []
        ac_keys = archive_counts.keys()
        ac_keys.sort(reverse=True)
        for year_month in ac_keys:
            date = '%s/01' % year_month
            archive_summary.append(dict(
                title=self.zLocalizedTime(DateTime('%s/01' % year_month)),
                number=archive_counts[year_month],
                url='%s?archiv=%s' % (self.context.absolute_url(), date),
                mark=self.request.get('archiv') == date,
            ))
        return archive_summary

    render = ViewPageTemplateFile('news_archive_portlet.pt')


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
