from ftw.contentpage.interfaces import IAddressBlock
from ftw.upgrade import UpgradeStep


class RemoveEmptyParagraphTagsInAddressBlocks(UpgradeStep):

    def __call__(self):
        query = {'object_provides': IAddressBlock.__identifier__}
        for obj in self.catalog_unrestricted_search(query, full_objects=True):
            if obj.getRawDirections() == '<p></p>':
                obj.setDirections('')
            if obj.getRawOpeningHours() == '<p></p>':
                obj.setOpeningHours('')
