**This repo is unmaintained. There are newer versions of Mattermost available on copr than in this repo**

This is a SPEC file for mattermost-desktop for Fedora and is used to create an RPM.

# Building
```
spectool -g *spec
fedpkg --release f26 local
```

# Installation
Installing it from Copr repo:
```
$ sudo dnf copr enable agoston/mattermost
$ sudo dnf install mattermost-desktop
```
Installing it if it was built using the SPEC file:
```
$ sudo rpm -Uvh mattermost-desktop-3.7.0-4.fc25.x86_64.rpm
```
