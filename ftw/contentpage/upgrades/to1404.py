from ftw.upgrade import UpgradeStep


class RemoveUploadJs(UpgradeStep):

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.contentpage.upgrades:1404', steps=['jsregistry', ])
