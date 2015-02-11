from ftw.upgrade import UpgradeStep
from ftw.contentpage.interfaces import IEventPage


class ReindexEventPage(UpgradeStep):

    def __call__(self):
        query = {'object_provides': IEventPage.__identifier__}
        self.catalog_reindex_objects(
            query,
            idxs=['start', 'end']
        )
