%global         debug_package %{nil}
%global         __strip /bin/true

# Remove bundled libraries from requirements/provides
%global         __requires_exclude ^(libvk_swiftshader.*\\.so.*|libEGL\\.so.*|libGLESv2\\.so.*)$
%global         __provides_exclude ^(lib.*\\.so.*)$

Name:           authy
Summary:        2-Factor Authentication
Version:        1.8.3
Release:        1%{?dist}
License:        https://www.spotify.com/legal/end-user-agreement
URL:            https://authy.com/
ExclusiveArch:  x86_64

# Get it with:
# curl -H 'Snap-Device-Series: 16' http://api.snapcraft.io/v2/snaps/info/authy | jq
Source0:        https://api.snapcraft.io/api/v1/snaps/download/H8ZpNgIoPyvmkgxOWw5MSzsXK1wRZiHn_5.snap

Source2:        authy-wrapper
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
%setup -q -c -T
unsquashfs -f -d . %{SOURCE0}

chrpath -d %{name}

sed -i -e 's/^Icon=.*/Icon=authy/g' meta/gui/%{name}.desktop

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_libdir}/%{name}

# Program resources
cp -frp authy locales resources swiftshader *.pak *.dat *.so *.bin \
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
* Thu Sep 10 2020 Simone Caronni <negativo17@gmail.com> - 1.8.3-1
- First build.
