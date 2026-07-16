%include vojtux_common.ks

# System language
lang cs_CZ.UTF-8
keyboard --xlayouts='cz'

# System timezone
timezone Europe/Prague --isUtc

%packages
tesseract-langpack-ces
tesseract-langpack-slk
hunspell-cs
%end

%post
#apply Vojtux customizations
git clone https://github.com/vojtapolasek/vojtux.git
cd vojtux/downloads
mkdir -p /etc/skel/.config
cp mimeapps.list /etc/skel/.config/
cp .tmux.conf /etc/skel/
cd /opt/
rm -rf vojtux

# setup symlink to documentation
ln -s /usr/share/doc/vojtux-docs-cs /etc/skel/dokumentace
ln -s /usr/share/doc/vojtux-docs-cs /home/liveuser/dokumentace
%end
