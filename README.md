# Lollypop (with transparent background)

[![Join the chat at https://gitter.im/gnumdk/lollypop](https://badges.gitter.im/gnumdk/lollypop.svg)](https://gitter.im/gnumdk/lollypop?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

![Lollypop logo](https://gitlab.gnome.org/gnumdk/lollypop/raw/master/data/icons/hicolor/256x256/apps/org.gnome.Lollypop.png)

Lollypop is a new GNOME music playing application.

- For users: https://wiki.gnome.org/Apps/Lollypop

- For packagers: You need to provide https://github.com/gnumdk/lollypop-portal

- FAQ: https://github.com/gnumdk/lollypop/wiki

For translators: https://hosted.weblate.org/projects/gnumdk/

It provides:

- MP3/4, ogg and FLAC.
- Genre/cover browsing
- Genre/artist/cover browsing
- Search
- Main playlist (called queue in other apps)
- Party mode
- Replay gain
- Cover art downloader
- Context artist view
- MTP sync
- Fullscreen view
- Radios support
- Last.fm support
- Auto install codecs
- HiDPI support
- TuneIn support

## Depends on

- `gtk3 >= 3.20`
- `gobject-introspection`
- `appstream-glib`
- `gir1.2-gstreamer-1.0 (Debian)`
- `python3`
- `meson >= 0.40`
- `ninja`
- `totem-plparser`
- `python-cairo`
- `python-gobject`
- `python-sqlite`
- `python-pylast >= 1.0`

## Installation (Archlinux)
Use this [PKGBUILD](https://gist.github.com/Rahix/7df4be58edea2895b9984ec43421c5b4).

## Building from git

```bash
$ git clone https://gitlab.gnome.org/gnumdk/lollypop.git
$ cd lollypop
$ meson builddir --prefix=/usr
# sudo ninja -C builddir install
```

In case you want the integration with [Last.fm](http://last.fm) to work you need to install `pylast`

```bash
# apt-get install python3-pip
# pip3 install pylast
```

### On Debian (Jessie)

```bash
$ git clone https://gitlab.gnome.org/gnumdk/lollypop.git
$ cd lollypop
# apt-get install meson libglib2.0-dev yelp-tools libgirepository1.0-dev libgtk-3-dev
$ meson builddir --prefix=/usr
# sudo ninja -C builddir install
```

### On Fedora

```bash
$ git clone https://gitlab.gnome.org/gnumdk/lollypop.git
$ cd lollypop
# sudo dnf install meson glib2-devel yelp-tools gtk3-devel gobject-introspection-devel python3
$ meson builddir --prefix=/usr
# sudo ninja -C builddir install
```
