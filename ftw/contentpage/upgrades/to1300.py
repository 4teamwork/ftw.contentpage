from ftw.upgrade import UpgradeStep


class UpdateSLView(UpgradeStep):
    """Add simplelayout_summary view
    """

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.contentpage.upgrades:1300')
