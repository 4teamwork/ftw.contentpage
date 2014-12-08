from ftw.upgrade import UpgradeStep


class InstallRecaptcha(UpgradeStep):

    def __call__(self):
        self.setup_install_profile(
            'profile-plone.formwidget.recaptcha:default')
