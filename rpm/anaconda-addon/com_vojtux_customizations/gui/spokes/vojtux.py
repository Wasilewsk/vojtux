"""GUI spoke for Vojtux customizations add-on."""

from pyanaconda.ui.gui.spokes import NormalSpoke
from pyanaconda.ui.gui import GUIObject

__all__ = ["VojtuxSpoke"]


class VojtuxSpoke(NormalSpoke, GUIObject):
    """GUI spoke for selecting Vojtux customizations."""

    builderObjects = ["vojtuxSpokeWindow"]
    mainFile = "spokes/vojtux.glade"
    translationTargetKeypath = "org_fedora_hello_world"

    icon = "accessories-dictionary-symbolic"
    title = "Vojtux _Customizations"

    def __init__(self, data, storage, payload, instclass):
        NormalSpoke.__init__(self, data, storage, payload, instclass)
        self.title = "Vojtux Customizations"
        self._apply_to_installed = None

    def initialize(self):
        NormalSpoke.initialize(self)
        self._apply_to_installed = self.builder.get_object("applyToInstalledCheck")

        addon_data = self.data.addons.com_vojtux_customizations

        self.builder.get_object("enableOrcaCheck").set_active(addon_data.enable_orca)
        self.builder.get_object("enableSpeechDispatcherCheck").set_active(addon_data.enable_speech_dispatcher)
        self.builder.get_object("enableRpmfusionCheck").set_active(addon_data.enable_rpmfusion)
        self.builder.get_object("enableVojtuxAppsCheck").set_active(addon_data.enable_vojtux_apps)
        self.builder.get_object("enableLightdmA11yCheck").set_active(addon_data.enable_lightdm_a11y)
        self.builder.get_object("setSelinuxPermissiveCheck").set_active(addon_data.set_selinux_permissive)

    def refresh(self):
        pass

    def apply(self):
        addon_data = self.data.addons.com_vojtux_customizations
        addon_data.enable_orca = self.builder.get_object("enableOrcaCheck").get_active()
        addon_data.enable_speech_dispatcher = self.builder.get_object("enableSpeechDispatcherCheck").get_active()
        addon_data.enable_rpmfusion = self.builder.get_object("enableRpmfusionCheck").get_active()
        addon_data.enable_vojtux_apps = self.builder.get_object("enableVojtuxAppsCheck").get_active()
        addon_data.enable_lightdm_a11y = self.builder.get_object("enableLightdmA11yCheck").get_active()
        addon_data.set_selinux_permissive = self.builder.get_object("setSelinuxPermissiveCheck").get_active()

    @property
    def mandatory(self):
        return False

    @property
    def completed(self):
        return True

    @property
    def status(self):
        count = 0
        addon_data = self.data.addons.com_vojtux_customizations
        if addon_data.enable_orca:
            count += 1
        if addon_data.enable_speech_dispatcher:
            count += 1
        if addon_data.enable_rpmfusion:
            count += 1
        if addon_data.enable_vojtux_apps:
            count += 1
        if addon_data.enable_lightdm_a11y:
            count += 1
        if addon_data.set_selinux_permissive:
            count += 1
        return "%d of 6 options enabled" % count
