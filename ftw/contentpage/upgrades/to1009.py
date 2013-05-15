from ftw.upgrade import UpgradeStep


class UpdateNewsAddableTypes(UpgradeStep):
    """Update News FTI
    """

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.contentpage.upgrades:1009')
