from ftw.upgrade import UpgradeStep


class UpdateRegistry(UpgradeStep):
    """Add show_mimetype_icon registry entry for alphabetical subject listing.
    """

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.contentpage.upgrades:1402')
