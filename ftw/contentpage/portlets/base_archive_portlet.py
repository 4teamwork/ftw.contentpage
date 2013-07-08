from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.i18nl10n import monthname_msgid
from Products.CMFPlone.utils import base_hasattr
from zope.i18n import translate


def zLocalizedTime(request, time, long_format=False):
    """Convert time to localized time
    """
    month_msgid = monthname_msgid(time.strftime("%m"))
    month = translate(month_msgid, domain='plonelocales',
                      context=request)

    return u"%s" % (month)


class ArchiveSummary(object):

    def __init__(self, context, request, interfaces, datefield, viewname):
        self.context = context
        self.request = request
        self.interfaces = interfaces
        self.datefield = datefield
        self.viewname = viewname
        self.selected_year = None
        self.selected_month = None

    def __call__(self):
        self._set_selected_archive()

        entries = self._get_archive_entries()
        counter = self._count_entries(entries)

        result = []
        year_numbers = sorted(counter, reverse=True)

        for year_number in year_numbers:

            year = counter.get(year_number)
            months = year.get('months')
            month_numbers = sorted(months, reverse=True)
            month_list = []

            for month_number in month_numbers:
                date = '%s/%s/01' % (year_number, month_number)

                month_list.append(dict(
                    title=zLocalizedTime(self.request, DateTime(date)),
                    number=months.get(month_number),
                    url=self._get_archive_url(date),
                    mark=[self.selected_year, self.selected_month] == [
                        year_number, month_number]
                ))

            result.append(dict(
                title=year_number,
                number=year.get('num'),
                months=month_list,
                mark=self.selected_year == year_number
            ))

        return result

    def _set_selected_archive(self):
        selected_archive = self.request.get('archive')
        if selected_archive:
            self.selected_year = selected_archive.split('/')[0]
            self.selected_month = selected_archive.split('/')[1]

    def _get_archive_url(self, date):
        return '%s/%s?archive=%s' % (
            self.context.absolute_url(),
            self.viewname,
            date)

    def _get_archive_entries(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(**self._get_query())

    def _get_query(self):
        query = {}
        if base_hasattr(self.context, 'getTranslations'):
            roots = self.context.getTranslations(
                review_state=False).values()
            root_path = ['/'.join(br.getPhysicalPath()) for br in roots]
            query['Language'] = 'all'
        else:
            root_path = '/'.join(self.context.getPhysicalPath())

        query['path'] = root_path
        query['object_provides'] = self.interfaces

        return query

    def _count_entries(self, entries):
        """Return a summary map like:

        {'2009': {
            'num': 6,
            'months': {
                '01': 4,
                '02': 2}
            }
        }
        """
        summary = {}

        for entry in entries:

            date = getattr(entry, self.datefield)
            if not date:
                continue

            if date.year() <= 1900:
                continue

            year_name = date.strftime('%Y')
            month_name = date.strftime('%m')

            year_summary = summary.get(year_name, {})
            month_summary = year_summary.get('months', {})

            # Increase month
            month_summary.update(
                {month_name: month_summary.get(month_name, 0) + 1})
            year_summary.update({'months': month_summary})

            # Increase year
            year_summary.update({'num': year_summary.get('num', 0) + 1})
            summary.update({year_name: year_summary})

        return summary
