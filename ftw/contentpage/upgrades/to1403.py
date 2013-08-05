from ftw.upgrade import UpgradeStep


class DndUpload(UpgradeStep):
    """Enable dnd upload on listingblock
    """

    def __call__(self):
        self.setup_install_profile(
            'profile-collective.quickupload:default')
