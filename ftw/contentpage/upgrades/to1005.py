from ftw.upgrade import UpgradeStep


class AddRoleMapEntrys(UpgradeStep):
    """Add missing rolemap entrys for the add permissions.
    """

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.contentpage.upgrades:1005')
