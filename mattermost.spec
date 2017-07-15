Name:       mattermost-desktop
Version:    3.7.0
Release:    1%{dist}
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

mv release/linux-unpacked/ release/%{name}
cd release/%{name}
./create_desktop_file.sh

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_libdir}/
mkdir -p %{buildroot}/%{_bindir}/
mkdir -p %{buildroot}/%{_datadir}/applications

cp -r release/%{name} %{buildroot}/%{_libdir}/
ln -s %{_libdir}/%{name} %{buildroot}/%{_bindir}/%{name}

desktop-file-install --dir=%{buildroot}/%{_datadir}/applications %{buildroot}/%{_libdir}/%{name}/Mattermost.desktop

%files
%{_bindir}/*
%{_libdir}/*
%{_datadir}/*

%doc README.md
%license LICENSE.txt

%changelog
* Sat Jul 15 2017 Agoston Szepessy <agoston@fedoraproject.org> - 1.0-1
- Initial version of SPEC file
