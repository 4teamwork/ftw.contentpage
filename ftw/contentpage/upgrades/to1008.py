from ftw.upgrade import UpgradeStep


class RemoveWorkflowFromBlocks(UpgradeStep):
    """Remove Workflow from TextBlock, ListingBlock, AddressBlock
    """

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.contentpage.upgrades:1008')

        self.remove_security_settings_from_blocks()

    def remove_security_settings_from_blocks(self):
        query = {'portal_type': ['ListingBlock', 'AddressBlock', 'TextBlock']}
        for obj in self.catalog_unrestricted_search(query, full_objects=True):
            for item in obj.ac_inherited_permissions(1):
                permission = item[0]
                obj.manage_permission(permission, roles=[], acquire=True)
                obj.reindexObjectSecurity()
