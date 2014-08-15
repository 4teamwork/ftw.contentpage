from ftw.upgrade import UpgradeStep
from ftw.contentpage.hooks import set_calendar_types


class SetCalendarTypes(UpgradeStep):

    def __call__(self):
        set_calendar_types(self.portal)
