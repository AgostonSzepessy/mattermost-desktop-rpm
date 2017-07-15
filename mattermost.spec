Name:       mattermost-desktop
Version:    3.7.0
Release:    1%{dist}
Summary:    Mattermost Desktop application for Linux.
URL:        https://about.mattermost.com/
License:    ASL 2.0

Source0:    https://github.com/mattermost/desktop/archive/v%{version}.tar.gz
BuildRequires: npm, nodejs, python, gcc-c++
Requires: gtk2, libXtst, libXScrnSaver, gconf-editor, nss, nspr, alsa-lib

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
mkdir -p %{buildroot}/%{_libdir}/
mkdir -p %{buildroot}/%{_bindir}/
cp -r release/linux-unpacked %{buildroot}/%{_libdir}/
ln -s %{_libdir}/%{name} %{buildroot}/%{_bindir}/%{name}

%files
%{buildroot}/%{_bindir}/*
%{buildroot}/%{_libdir}/*
%doc README.md
%license LICENSE.txt

%changelog
