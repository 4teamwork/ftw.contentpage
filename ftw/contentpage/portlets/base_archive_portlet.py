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

    return u"%s %s" % (month, time.strftime('%Y'))

def archive_summary(context, request, contenttype, datefield):
    """Returns an ordered list of summary infos per month."""
    catalog = getToolByName(context, 'portal_catalog')
    query = {}
    if base_hasattr(context, 'getTranslations'):
        roots = context.getTranslations(
            review_state=False).values()
        root_path = ['/'.join(br.getPhysicalPath()) for br in roots]
        query['Language'] = 'all'
    else:
        root_path = '/'.join(context.getPhysicalPath())

        query['path'] = root_path
        query['portal_type'] = contenttype

        archive_counts = {}
        entries = catalog(**query)
        for entry in entries:
            year_month = getattr(entry, datefield).strftime('%Y/%m')
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
                    title=zLocalizedTime(request, DateTime('%s/01' % year_month)),
                    number=archive_counts[year_month],
                    url='%s?archiv=%s' % (context.absolute_url(), date),
                    mark=request.get('archiv') == date,
                    ))
        return archive_summary
