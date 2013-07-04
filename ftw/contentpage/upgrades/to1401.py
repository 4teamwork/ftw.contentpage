from ftw.upgrade import UpgradeStep


class UpdateRegistry(UpgradeStep):
    """Add alphabetical subject listing configuration to registry.
    """

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.contentpage.upgrades:1401')
