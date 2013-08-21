from ftw.upgrade import UpgradeStep


class InstallBrowserlayer(UpgradeStep):

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.contentpage.upgrades:1405', steps=['browserlayer', ])
