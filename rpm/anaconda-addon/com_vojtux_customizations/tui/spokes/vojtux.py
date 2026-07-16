"""TUI spoke for Vojtux customizations add-on."""

from pyanaconda.ui.tui.spokes import NormalTUISpoke
from pyanaconda.ui.tui.tuiobject import TUIObject

__all__ = ["VojtuxTUISpoke"]


class VojtuxTUISpoke(NormalTUISpoke):
    """TUI spoke for selecting Vojtux customizations."""

    title = "Vojtux Customizations"
    category = "Vojtux"

    def __init__(self, data, storage, payload, instclass):
        NormalTUISpoke.__init__(self, data, storage, payload, instclass)
        self._selections = {}
        self._apply_to_installed = None

    def initialize(self):
        NormalTUISpoke.initialize(self)
        addon_data = self.data.addons.com_vojtux_customizations
        self._selections = {
            "orca": addon_data.enable_orca,
            "speech-dispatcher": addon_data.enable_speech_dispatcher,
            "rpmfusion": addon_data.enable_rpmfusion,
            "vojtux-apps": addon_data.enable_vojtux_apps,
            "lightdm-a11y": addon_data.enable_lightdm_a11y,
            "selinux-permissive": addon_data.set_selinux_permissive,
        }

    def refresh(self, args=None):
        NormalTUISpoke.refresh(self, args)

        from pyanaconda.ui.tui.utils import InputMap
        from pyanaconda.core.i18n import _

        self._window = self._create_new_window()

        text = _("Select Vojtux customizations to apply:\n\n")
        for i, (key, label) in enumerate(self._get_options()):
            status = "[x]" if self._selections[key] else "[ ]"
            text += "%d. %s %s\n" % (i + 1, status, label)

        text += "\n"
        text += _("Press a number to toggle, 0 to confirm, c to cancel\n")

        self._window.set_text(text)

    def _get_options(self):
        return [
            ("orca", "Enable Orca screen reader on login"),
            ("speech-dispatcher", "Enable speech-dispatcher espeak-ng module"),
            ("rpmfusion", "Enable RPM Fusion repositories"),
            ("vojtux-apps", "Enable Vojtux-apps Copr repository"),
            ("lightdm-a11y", "Configure LightDM for accessibility"),
            ("selinux-permissive", "Set SELinux to permissive mode"),
        ]

    def input(self, key):
        options = self._get_options()

        try:
            num = int(key)
        except ValueError:
            return NormalTUISpoke.input(self, key)

        if num == 0:
            self.apply()
            self.close()
            return True
        elif 1 <= num <= len(options):
            key_name = options[num - 1][0]
            self._selections[key_name] = not self._selections[key_name]
            self.redraw()
            return True

        return NormalTUISpoke.input(self, key)

    def apply(self):
        addon_data = self.data.addons.com_vojtux_customizations
        addon_data.enable_orca = self._selections["orca"]
        addon_data.enable_speech_dispatcher = self._selections["speech-dispatcher"]
        addon_data.enable_rpmfusion = self._selections["rpmfusion"]
        addon_data.enable_vojtux_apps = self._selections["vojtux-apps"]
        addon_data.enable_lightdm_a11y = self._selections["lightdm-a11y"]
        addon_data.set_selinux_permissive = self._selections["selinux-permissive"]

    @property
    def mandatory(self):
        return False

    @property
    def completed(self):
        return True

    @property
    def status(self):
        count = sum(1 for v in self._selections.values() if v)
        return "%d of %d options enabled" % (count, len(self._selections))
