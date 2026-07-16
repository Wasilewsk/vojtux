Name:     anaconda-addon-vojtux
Version:  1
Release:  1%{?dist}
Summary:  Vojtux customizations add-on for the Anaconda installer
License:  GPLv2+
URL:      https://github.com/vojtapolasek/vojtux

Source0:  com_vojtux_customizations/
Source1:  org.fedoraproject.Anaconda.Addons.VojtuxCustomizations.service
Source2:  org.fedoraproject.Anaconda.Addons.VojtuxCustomizations.conf

BuildArch: noarch
BuildRequires: python3-devel
Requires: anaconda >= 34

%description
Anaconda installer add-on that provides a configuration screen for
Vojtux accessibility customizations during system installation.
Users can choose to enable Orca screen reader, speech-dispatcher,
RPM Fusion repos, Vojtux-apps repo, LightDM accessibility, and
SELinux permissive mode.

%install
install -d %{buildroot}%{_datadir}/anaconda/addons/com_vojtux_customizations
cp -r %{SOURCE0}/* %{buildroot}%{_datadir}/anaconda/addons/com_vojtux_customizations/

install -d %{buildroot}%{_datadir}/anaconda/dbus/services
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/anaconda/dbus/services/

install -d %{buildroot}%{_datadir}/anaconda/dbus/confs
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/anaconda/dbus/confs/

%files
%{_datadir}/anaconda/addons/com_vojtux_customizations/
%{_datadir}/anaconda/dbus/services/org.fedoraproject.Anaconda.Addons.VojtuxCustomizations.service
%{_datadir}/anaconda/dbus/confs/org.fedoraproject.Anaconda.Addons.VojtuxCustomizations.conf

%changelog
* Thu Jul 16 2026 Vojtux Contributors - 1-1
- Initial package
- Provides GUI and TUI spokes for Vojtux customizations
- Supports kickstart configuration via %addon section
