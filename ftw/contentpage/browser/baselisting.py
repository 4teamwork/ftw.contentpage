from DateTime import DateTime
from DateTime.interfaces import SyntaxError as dtSytaxError
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from zope.publisher.browser import BrowserView


def extend_query_by_date(query, datestring, date_field):
    try:
        start = DateTime(datestring)
    except dtSytaxError:
        return query
    end = DateTime('%s/%s/%s' % (start.year() + start.month() / 12,
                                 start.month() % 12 + 1, 1))
    end = end - 1
    query[date_field] = {'query': (start.earliestTime(),
                                    end.latestTime()),
                          'range': 'minmax'}
    return query


class BaseListing(BrowserView):

    def __init__(self, context, request):
        super(BaseListing, self).__init__(context, request)
        self.batch = None

    def __call__(self):
        b_start = self.request.form.get('b_start', 0)
        self.batch = Batch(self.get_items(), 10,
                           b_start)
        return self.template()

    def get_creator(self, item):
        memberid = item.Creator
        mt = getToolByName(self.context, 'portal_membership')
        member_info = mt.getMemberInfo(memberid)
        if member_info:
            fullname = member_info.get('fullname', '')
        else:
            fullname = None
        if fullname:
            return fullname
        else:
            return memberid

    def search_results(self, query, date_field):
        """Get all news items"""

        # Implement archive functionality - used by the archive portlet
        context = self.context
        ct = context.portal_type
        datestring = self.request.get('archive')
        if datestring:
            query = extend_query_by_date(query, datestring, date_field)

        if ct == 'Topic':
            return context.queryCatalog()
        else:
            catalog = getToolByName(context, 'portal_catalog')
            query['path'] = '/'.join(context.getPhysicalPath())
            return catalog(query)

    def has_img(self, brain):
        """ Checks if the news have an image.
        """
        return bool(brain.getObject().getImage())

    def get_img(self, brain):
        obj = brain.getObject()
        scale = obj.restrictedTraverse('@@images')
        return scale.scale(
            'image',
            width=100,
            height=100).tag(**{'class': 'tileImage'})
