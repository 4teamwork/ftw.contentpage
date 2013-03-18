from ftw.upgrade import UpgradeStep


class RemoveIcons(UpgradeStep):
    """Installs the profile which removes the icon expressions from
    simplelayout actions.
    """
    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.contentpage.upgrades:1002')
