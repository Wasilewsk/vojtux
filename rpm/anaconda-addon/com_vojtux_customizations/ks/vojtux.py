"""Kickstart support for Vojtux customizations add-on."""

from pyanaconda.addons import AddonData
from pyanaconda.constants import getSysroot

from pykickstart.options import KSOptionParser
from pykickstart.errors import KickstartParseError, formatErrorMsg


class VojtuxData(AddonData):
    """Data class for Vojtux customizations."""

    def __init__(self, name):
        AddonData.__init__(self, name)
        self.enable_orca = True
        self.enable_speech_dispatcher = True
        self.enable_rpmfusion = True
        self.enable_vojtux_apps = True
        self.enable_lightdm_a11y = True
        self.set_selinux_permissive = True

    def handle_header(self, args, lineInfo=None):
        """Handle the %addon header line."""
        AddonData.handle_header(self, args, lineInfo)

        op = KSOptionParser()
        op.add_option("--enable-orca", type="boolean", default=True,
                      help="Enable Orca screen reader on login")
        op.add_option("--enable-speech-dispatcher", type="boolean", default=True,
                      help="Enable speech-dispatcher espeak-ng module")
        op.add_option("--enable-rpmfusion", type="boolean", default=True,
                      help="Enable RPM Fusion repositories")
        op.add_option("--enable-vojtux-apps", type="boolean", default=True,
                      help="Enable Vojtux-apps Copr repository")
        op.add_option("--enable-lightdm-a11y", type="boolean", default=True,
                      help="Configure LightDM for accessibility")
        op.add_option("--set-selinux-permissive", type="boolean", default=True,
                      help="Set SELinux to permissive mode")

        opts = self.parser.parse_args(args=args)[0]
        self.enable_orca = opts.enable_orca
        self.enable_speech_dispatcher = opts.enable_speech_dispatcher
        self.enable_rpmfusion = opts.enable_rpmfusion
        self.enable_vojtux_apps = opts.enable_vojtux_apps
        self.enable_lightdm_a11y = opts.enable_lightdm_a11y
        self.set_selinux_permissive = opts.set_selinux_permissive

    def handle_line(self, line):
        """Handle lines inside the %addon section."""
        pass

    def setup(self, storage, ksdata, instclass, payload):
        """Setup before installation transaction."""
        pass

    def execute(self, storage, ksdata, instclass, users, payload):
        """Execute post-installation tasks on the target system."""
        import os
        import shutil

        sysroot = getSysroot()

        if self.enable_speech_dispatcher:
            speechd_conf = os.path.join(sysroot, "etc/speech-dispatcher/speechd.conf")
            if os.path.exists(speechd_conf):
                with open(speechd_conf, "r") as f:
                    content = f.read()
                old = '#AddModule "espeak-ng"                "sd_espeak-ng" "espeak-ng.conf"'
                new = 'AddModule "espeak-ng"                "sd_espeak-ng" "espeak-ng.conf"'
                if old in content:
                    content = content.replace(old, new)
                    with open(speechd_conf, "w") as f:
                        f.write(content)

        if self.enable_lightdm_a11y:
            wrapper_path = os.path.join(sysroot, "usr/local/bin/orca-login-wrapper")
            with open(wrapper_path, "w") as f:
                f.write("#!/bin/bash\n\namixer -c 0 set Master playback 50% unmute\n/usr/bin/orca &\n")
            os.chmod(wrapper_path, 0o755)

            lightdm_conf = os.path.join(sysroot, "etc/lightdm/lightdm-gtk-greeter.conf")
            greeter_config = (
                "\n[greeter]\n"
                "background = /usr/share/backgrounds/default.png\n"
                "reader = /usr/local/bin/orca-login-wrapper\n"
                "a11y-states = +reader\n"
            )
            if os.path.exists(lightdm_conf):
                with open(lightdm_conf, "a") as f:
                    f.write(greeter_config)
            else:
                with open(lightdm_conf, "w") as f:
                    f.write(greeter_config)

        if self.enable_rpmfusion or self.enable_vojtux_apps:
            rpm_dir = os.path.join(sysroot, "etc/yum.repos.d")
            os.makedirs(rpm_dir, exist_ok=True)

        if self.enable_vojtux_apps:
            repo_file = os.path.join(rpm_dir, "vojtux-apps.repo")
            repo_content = (
                "[vojtux-apps]\n"
                "name=Copr repo for vojtux-apps owned by tyrylu\n"
                "baseurl=https://copr-be.cloud.fedoraproject.org/results/tyrylu/vojtux-apps/fedora-44-x86_64/\n"
                "type=rpm-md\n"
                "skip_if_unavailable=True\n"
                "enabled=1\n"
                "gpgcheck=1\n"
                "gpgkey=https://copr-be.cloud.fedoraproject.org/results/tyrylu/vojtux-apps/pubkey.gpg\n"
                "repo_gpgcheck=0\n"
                "module_hotfixes=1\n"
            )
            with open(repo_file, "w") as f:
                f.write(repo_content)

        if self.set_selinux_permissive:
            selinux_conf = os.path.join(sysroot, "etc/selinux/config")
            if os.path.exists(selinux_conf):
                with open(selinux_conf, "r") as f:
                    content = f.read()
                content = content.replace("SELINUX=enforcing", "SELINUX=permissive")
                with open(selinux_conf, "w") as f:
                    f.write(content)

    def __str__(self):
        """Generate kickstart representation."""
        parts = []
        parts.append("enable-orca=%s" % self.enable_orca)
        parts.append("enable-speech-dispatcher=%s" % self.enable_speech_dispatcher)
        parts.append("enable-rpmfusion=%s" % self.enable_rpmfusion)
        parts.append("enable-vojtux-apps=%s" % self.enable_vojtux_apps)
        parts.append("enable-lightdm-a11y=%s" % self.enable_lightdm_a11y)
        parts.append("set-selinux-permissive=%s" % self.set_selinux_permissive)
        return " ".join(parts)
