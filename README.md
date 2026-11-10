# Pyinotify

* License          : MIT
* Project URL      : [http://github.com/seb-m/pyinotify](http://github.com/seb-m/pyinotify)
* This Fork's URL  : [http://github.com/keithbowes/pyinotify](http://github.com/keithbowes/pyinotify)
* Project Wiki     : [http://github.com/seb-m/pyinotify/wiki](http://github.com/seb-m/pyinotify/wiki)
* API Documentation: [https://seb.dbzteam.org/pyinotify/](https://seb.dbzteam.org/pyinotify/)


## Dependencies

* Python ≥ 3.0
* One of the following systems:

    * A Linux distro running Linux ≥ 2.6.27.
    * FreeBSD  ≥ 14.4.
    * MacOS X or a BSD distribution (including versions of FreeBSD older than 14.3) with
      [libinotify](https://github.com/libinotify-kqueue/libinotify-kqueue). The GitHub actions don't
      detect any events but it might work on your computer.


## Install

### Get version 0.9.6 from PyPI and install it with `pip`

    # To install pip follow http://www.pip-installer.org/en/latest/installing.html
    $ pip install pyinotify

### Alternatively, get the elephant fork

    $ pip install pyinotify-elephant-fork

### Or install pyinotify directly from source

    $ make deps install

## Watch a directory

Install pyinotify and run this command from a shell:

    $ python -m pyinotify -v /my-dir-to-watch
