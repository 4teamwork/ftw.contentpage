from ftw.upgrade import UpgradeStep


class UpdateRolemapAndFactoryTool(UpgradeStep):
    """Update rolemap and factory tool
    """

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.contentpage.upgrades:1006')
