from ftw.upgrade import UpgradeStep


class UpdateAddressBlockFTI(UpgradeStep):
    """Update AddressBlock FTI
    """

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.contentpage.upgrades:1007')
