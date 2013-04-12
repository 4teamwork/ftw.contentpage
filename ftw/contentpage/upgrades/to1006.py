from ftw.upgrade import UpgradeStep


class UpdateRolemap(UpgradeStep):
    """Update rolemap
    """

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.contentpage.upgrades:1006')
