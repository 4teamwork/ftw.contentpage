from ftw.upgrade import UpgradeStep


class AddEventType(UpgradeStep):
    """Installs the profile which adds a registry entry for default
     table columns
    """

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.contentpage.upgrades:1004')
