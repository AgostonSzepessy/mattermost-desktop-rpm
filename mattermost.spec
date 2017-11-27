Name:       mattermost-desktop
Version:    3.7.1
Release:    2%{dist}
Summary:    Mattermost Desktop application for Linux.
URL:        https://about.mattermost.com/
License:    ASL 2.0
BuildArch:  x86_64 i386

Source0:    https://github.com/mattermost/desktop/archive/v%{version}.tar.gz
BuildRequires: npm, nodejs, python, gcc-c++, git, desktop-file-utils
Requires: gtk2, libXtst, libXScrnSaver, gconf-editor, nss, nspr, alsa-lib

# Exclude libffmpeg.so()(64bit) because DNF cannot find this file in any package
%define __requires_exclude ^libffmpeg.so

%global debug_package %{nil}

%description
Open source, private cloud Slack-alternative, workplace messaging for web, PCs and phones.

%prep
%autosetup -n desktop-%{version}

# Reduce build time by removing creation of Debian package
# Taken from: https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=mattermost-desktop
sed -i -e '/^[[:space:]]*"target": \[/!b' -e '$!N;s/\n[[:space:]]*"deb",//' electron-builder.json

# Depending on architecture, remove either ia32 or x86_64 build to speed up build time
# Taken from: https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=mattermost-desktop
%ifarch i386
%define releasedir linux-ia32-unpacked
sed -i 's/build --linux --x64 --ia32/build --linux --ia32/g' package.json
%endif

%ifarch x86_64
%define releasedir linux-unpacked
sed -i 's/build --linux --x64 --ia32/build --linux --x64/g' package.json
%endif

%build
npm install
npm run build
npm run package:linux

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_libdir}/%{name}
mkdir -p %{buildroot}/%{_bindir}/
mkdir -p %{buildroot}/%{_datadir}/applications
mkdir -p %{buildroot}/%{_datadir}/pixmaps

mv release/%{releasedir} release/%{name}
cd release/%{name}
rm create_desktop_file.sh

mv icon.png %{name}.png

echo "[Desktop Entry]" >> %{name}.desktop
echo "Name=Mattermost" >> %{name}.desktop
echo "Comment=Mattermost Desktop application for Linux" >> %{name}.desktop
echo "Exec="%{name} >> %{name}.desktop
echo "Terminal=false" >> %{name}.desktop
echo "Type=Application" >> %{name}.desktop
echo "Icon="%{_datadir}/pixmaps/%{name}.png >> %{name}.desktop
echo "Categories=Network;Application;" >> %{name}.desktop

cp -r * %{buildroot}/%{_libdir}/%{name}
ln -s %{_libdir}/%{name}/%{name} %{buildroot}/%{_bindir}/%{name}

cp %{name}.png %{buildroot}/%{_datadir}/pixmaps/

desktop-file-install --dir=%{buildroot}/%{_datadir}/applications %{buildroot}/%{_libdir}/%{name}/%{name}.desktop

%files
%{_bindir}/*
%{_libdir}/*
%{_datadir}/*

%doc README.md
%license LICENSE.txt NOTICE.txt

%changelog
* Sun Nov 26 2017 Agoston Szepessy <agoston@fedoraproject.org> - 3.7.1-2
- Remove libffmpeg.so()(64bit) from automatic RPM dependency requirements
* Fri Sep 08 2017 Agoston Szepessy <agoston@fedoraproject.org> - 3.7.1-1
- Update to new version and add build optimizations.
* Sat Jul 22 2017 Agoston Szepessy <agoston@fedoraproject.org> - 3.7.0-5
- Add i386 build option
* Thu Jul 20 2017 Agoston Szepessy <agoston@fedoraproject.org> - 3.7.0-4
- Clean up spec file and add other license section
* Wed Jul 19 2017 Agoston Szepessy <agoston@fedoraproject.org> - 3.7.0-3
- Fix error in desktop file icon generation
* Tue Jul 18 2017 Agoston Szepessy <agoston@fedoraproject.org> - 3.7.0-2
- Fix desktop file
* Sat Jul 15 2017 Agoston Szepessy <agoston@fedoraproject.org> - 3.7.0-1
- Initial version of SPEC file
