# Pyinotify

* License          : MIT
* Project URL      : [http://github.com/seb-m/pyinotify](http://github.com/seb-m/pyinotify)
* Project Wiki     : [http://github.com/seb-m/pyinotify/wiki](http://github.com/seb-m/pyinotify/wiki)
* API Documentation: [http://seb-m.github.com/pyinotify](http://seb-m.github.com/pyinotify)


## Dependencies

* Linux ≥ 2.6.13 or another *nix with inotify support
* Python ≥ 3.0


## Install

### Get version 0.9.6 from PyPI and install it with `pip`

    # To install pip follow http://www.pip-installer.org/en/latest/installing.html
    $ pip install pyinotify

### Alternatively, get the elephant fork

    $ pip install pyinotify-elephant-fork

### Or install pyinotify directly from source

    $ python -m build -nw
    $ pip install .

## Watch a directory

Install pyinotify and run this command from a shell:

    $ python -m pyinotify -v /my-dir-to-watch
