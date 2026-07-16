%include fedora-live-base.ks
%include repos.ks
%include fedora-mate-common.ks

selinux --disabled

# add group because of brltty
group --name brlapi

# System services
services --enabled="chronyd,brltty"

part / --size 10240 --fstype ext4

%packages
#customizations for Vojtux

#additional software for Vojtux
pidgin
xsane
chromium
mate-menu
#hardware support
@hardware-support
gutenprint-cups
cups-filters
foomatic-db
foomatic-db-ppds
splix
hplip
xorg-x11-drv-nouveau
libsane-hpaio
xorg-x11-server-Xvfb
xorg-x11-drv-dummy
#more software
audacity
soundconverter
ifuse
git
curl
@vlc
sed
wget
jmtpfs
nano
speech-dispatcher-utils
soundconverter
tmux
unrar
timidity++
#display manager
-slick-greeter
-slick-greeter-mate
lightdm-gtk-greeter
lightdm-gtk-greeter-settings
#ocr
lios
toggle-monitor

# settings and shortcuts
vojtux-settings
sox
# OCR desktop
ocrdesktop
ocrmypdf

# a11y sound theme
a11y-sound-theme

# remote support
tmate

# pandoc for document conversion and also used during testing
pandoc

# brltty-xw for testing braille output without a physical device
brltty-xw

# Anaconda addon for Vojtux customizations during installation
anaconda-addon-vojtux
%end

%addon com_vojtux_customizations
enable-orca = True
enable-speech-dispatcher = True
enable-rpmfusion = True
enable-vojtux-apps = True
enable-lightdm-a11y = True
set-selinux-permissive = True
%end

# copied from fedora-live-mate-compiz.ks
%post
# set livesys session type
sed -i 's/^livesys_session=.*/livesys_session="mate"/' /etc/sysconfig/livesys

%end

%post
# configure temporary dns
cat >> /etc/resolv.conf << EOM
nameserver 8.8.8.8
nameserver 8.8.4.4
EOM


#rpm fusion keys
echo "== RPM Fusion Free: Base section =="
echo "Importing RPM Fusion keys"
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-free-fedora-*-primary
echo "Importing RPM Fusion keys"
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-nonfree-fedora-*-primary

# import Vojtux-apps key
dnf copr enable -y tyrylu/vojtux-apps

echo "Updating dconf databases..."
dconf update

#configure speech dispatcher
sed -i 's/#AddModule "espeak-ng"                "sd_espeak-ng" "espeak-ng.conf"/AddModule "espeak-ng"                "sd_espeak-ng" "espeak-ng.conf"/' /etc/speech-dispatcher/speechd.conf

#setup lightdm
# create a wrapper script which makes sure that sound is unmuted and at 50% on login screen
cat > /usr/local/bin/orca-login-wrapper <<EOM
#!/bin/bash

amixer -c 0 set Master playback 50% unmute
/usr/bin/orca &

EOM
chmod 755 /usr/local/bin/orca-login-wrapper
cat >> /etc/lightdm/lightdm-gtk-greeter.conf <<EOM
[greeter]
background = /usr/share/backgrounds/default.png
reader = /usr/local/bin/orca-login-wrapper
a11y-states = +reader

EOM

# disable temporary dns
echo "" > /etc/resolv.conf

%end
