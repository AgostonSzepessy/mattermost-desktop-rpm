Name:       mattermost-desktop
Version:    3.7.0
Release:    4%{dist}
Summary:    Mattermost Desktop application for Linux.
URL:        https://about.mattermost.com/
License:    ASL 2.0
BuildArch:	x86_64
Source0:    https://github.com/mattermost/desktop/archive/v%{version}.tar.gz
BuildRequires: npm, nodejs, python, gcc-c++, git, desktop-file-utils
Requires: gtk2, libXtst, libXScrnSaver, gconf-editor, nss, nspr, alsa-lib

%global debug_package %{nil}

%description
Open source, private cloud Slack-alternative, workplace messaging for web, PCs and phones.

%prep
%autosetup -n desktop-%{version}
sed -i -e '/^[[:space:]]*"target": \[/!b' -e '$!N;s/\n[[:space:]]*"deb",//' electron-builder.json

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

mv release/linux-unpacked/ release/%{name}
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
* Thu Jul 20 2017 Agoston Szepessy <agoston@fedoraproject.org> - 1.0-4
- Clean up spec file and add other license section
* Wed Jul 19 2017 Agoston Szepessy <agoston@fedoraproject.org> - 1.0-3
- Fix error in desktop file icon generation
* Tue Jul 18 2017 Agoston Szepessy <agoston@fedoraproject.org> - 1.0-2
- Fix desktop file
* Sat Jul 15 2017 Agoston Szepessy <agoston@fedoraproject.org> - 1.0-1
- Initial version of SPEC file
