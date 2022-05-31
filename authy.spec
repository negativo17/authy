%global         debug_package %{nil}
%global         __strip /bin/true
# Build id links are sometimes in conflict with other RPMs.
%define         _build_id_links none

# Remove bundled libraries from requirements/provides
%global         __requires_exclude ^(libvk_swiftshader.*\\.so.*|libEGL\\.so.*|libGLESv2\\.so.*|libffmpeg\\.so.*)$
%global         __provides_exclude ^(lib.*\\.so.*)$

Name:           authy
Summary:        2-Factor Authentication
Version:        2.2.0
Release:        1%{?dist}
License:        https://www.spotify.com/legal/end-user-agreement
URL:            https://authy.com/
ExclusiveArch:  x86_64

Source0:        %{name}-%{version}.tar.xz
Source1:        %{name}-tarball.py

Source2:        %{name}-wrapper
#Source4:        authy.appdata.xml

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
#BuildRequires:  libappstream-glib
BuildRequires:  squashfs-tools

Requires:       hicolor-icon-theme
# Chrome Embedded Framework dynamically loads libXss.so.1:
Requires:       libXScrnSaver%{?_isa}

%description
The Twilio Authy app generates secure 2 step verification tokens on your device.
It help’s you protect your account from hackers and hijackers by adding an
additional layer of security.

Secure Cloud Backups: Did you lose your device and got locked out of all of your
accounts? Twilio Authy provides secure cloud encrypted backups so you will never
lose access to your tokens again. We use the same algorithm banks and the NSA
use to protect their information.

Multi Device Synchronization: Are your re-scanning all your QR codes just to add
them to your tablet and smartphone? With Twilio Authy you can simply add devices
to your account and all of your 2FA tokens will automatically synchronize.

%prep
%autosetup

chrpath -d %{name}

sed -i -e 's/^Icon=.*/Icon=authy/g' meta/gui/%{name}.desktop

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_libdir}/%{name}

# Program resources
cp -frp %{name} locales resources swiftshader *.pak *.dat *.so *.bin \
    %{buildroot}%{_libdir}/%{name}

# Set permissions
find %{buildroot}%{_libdir}/%{name} -name "*.so" -exec chmod 755 {} \;
chmod 755 %{buildroot}%{_libdir}/%{name}/%{name}

# Wrapper script
mkdir -p %{buildroot}%{_bindir}
cat %{SOURCE2} | sed -e 's|INSTALL_DIR|%{_libdir}/%{name}|g' \
    > %{buildroot}%{_bindir}/%{name}
chmod +x %{buildroot}%{_bindir}/%{name}

# Desktop file
install -m 0644 -D -p meta/gui/%{name}.desktop \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

# Icons
install -p -D -m 644 meta/gui/icon.png \
    %{buildroot}%{_datadir}/pixmaps/%{name}.png

## Install AppData
#mkdir -p %{buildroot}%{_metainfodir}/
#install -p -m 0644 %{SOURCE4} %{buildroot}%{_metainfodir}/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
#appstream-util validate-relax --nonet %{buildroot}/%{_metainfodir}/%{name}.appdata.xml

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_libdir}/%{name}
#%{_metainfodir}/%{name}.appdata.xml

%changelog
* Tue May 31 2022 Simone Caronni <negativo17@gmail.com> - 2.2.0-1
- Update to version 2.2.0.

* Thu Mar 10 2022 Simone Caronni <negativo17@gmail.com> - 2.1.0-1
- Update to version 2.1.0.

* Mon Dec 13 2021 Simone Caronni <negativo17@gmail.com> - 1.9.0-2
- Fix build id links in conflict with other RPMs.

* Sat Nov 20 2021 Simone Caronni <negativo17@gmail.com> - 1.9.0-1
- Update to version 1.9.0.

* Sat Jul 24 2021 Simone Caronni <negativo17@gmail.com> - 1.8.4-1
- Update to 1.8.4.

* Sun Oct 25 2020 Simone Caronni <negativo17@gmail.com> - 1.8.3-2
- Fix library filter.

* Thu Sep 10 2020 Simone Caronni <negativo17@gmail.com> - 1.8.3-1
- First build.
