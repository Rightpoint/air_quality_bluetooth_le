Air Quality Bluetooth LE
========================

[![CircleCI](https://img.shields.io/circleci/project/github/Raizlabs/air_quality_bluetooth_le/master.svg)](https://circleci.com/gh/Raizlabs/air_quality_bluetooth_le)
[![image](https://img.shields.io/pypi/v/aqi_ble.svg)](https://pypi.python.org/pypi/aqi_ble)
[![image](https://img.shields.io/travis/Raizlabs/aqi_ble.svg)](https://travis-ci.org/Raizlabs/aqi_ble)
[![Documentation Status](https://readthedocs.org/projects/aqi-ble/badge/?version=latest)](https://aqi-ble.readthedocs.io/en/latest/?badge=latest)


Bluetooth Low Energy interface for SDS011 APM2.5 air quality sensor

## Features

-   TODO

## Quick Start

### Setup

Install [Python 3.6](https://www.python.org/) (or higher) and [Pipenv](https://github.com/pypa/pipenv) to manage Python dependencies.

macOS:

```
$ brew install python3
$ pip3 install -U pipenv
```

If you're using macOS you'll also need to install a driver for the SDS011 particle sensor's USB TTY interface: [CH341SER_MAC.ZIP](https://github.com/chrisballinger/sds011-rs/raw/master/CH341SER_MAC.ZIP).

Linux:

```
$ sudo apt-get install python3-pip
$ pip3 install -U pipenv
```

Then clone the repo and run `pipenv` to install the dependencies:

```
$ git clone https://github.com/Raizlabs/air_quality_bluetooth_le.git
$ cd air_quality_bluetooth_le/
$ pipenv install --dev
```

### Running

You'll need to pass the path to the USB TTY device. If you're not sure where it is, try `ls /dev/tty*` and look for an entry with `usb` somewhere in the name. On Linux this is usually `/dev/ttyUSB0`. On macOS it can vary, but it will usually

```bash
$ ls /dev/tty*
```

To try it out use `pipenv shell` to activate the virtual environment:

```bash
$ pipenv shell
```

You can list all the options with `cli.py --help`:

```bash
$ ./cli.py --help
Usage: cli.py [OPTIONS]

Options:
  -p, --path PATH              Path to USB TTY sensor device. e.g.
                               /dev/ttyUSB0  [required]
  --json_keyfile PATH          Path to Google OAuth JSON Keyfile
  --sheet_url TEXT             Google Sheets URL
  --coordinate FLOAT...        GPS Coordinate (Latitude Longitude) e.g.
                               37.8066073985003 -122.27042233335567
  --elevation FLOAT            Sensor Elevation in Meters e.g. 40
  --name TEXT                  Sensor Name e.g. Bedroom
  --remote_debug_secret TEXT   Remote Debugging attachment secret e.g.
                               my_secret
  --remote_debug_address TEXT  Remote Debugging IP e.g. 0.0.0.0
  --remote_debug_port INTEGER  Remote Debugging port e.g. 3000
  --remote_debug_wait BOOLEAN  Wait for Remote Debugger to attach
  --help                       Show this message and exit.
```

Then run our command line program to read out the sensor values:

```
# macOS
$ python cli.py -p /dev/tty.wchusbserial1420
# Linux
$ python cli.py -p /dev/ttyUSB0
```

#### Google Sheets

Create Google OAuth2 Signed Credentails: http://gspread.readthedocs.io/en/latest/oauth2.html

Place credentials file in `private_keys/sheets-api-key.json`, we will use this later for the `json_keyfile` path.

Create a new Google Sheet and share it (edit access) with the email listed for `client_email` in `sheets-api-key.json`. Copy the Share URL of the Google Sheet, which we will use for `sheet_url`.

Pass the path to `json_keyfile` and `sheet_url`

```
$ python aqi_ble/cli.py -p /dev/tty.wchusbserial1420 --name "RZWest" --coordinate 37.8066073985003 -122.27042233335567 --elevation 57.6072 --json_keyfile private_keys/sheets-api-key.json --sheet_url https://docs.google.com/spreadsheets/d/1F_1LBbbF...LzYhv-SB2QGZv0
```

## Configuring VS Code

Go to the Plugins tab and add the official [Python plugin](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

Next we'll get the Pipenv virtual environment and set it up for VS Code.

```bash
$ pipenv --venv
/Users/username/.local/share/virtualenvs/air_quality_bluetooth_le-PO89Jxuj
```

Edit Workspace settings `python.pythonPath`, using the value on your machine from `pipenv --venv` above with `bin/python` appended to the end.

```json
{
    "python.pythonPath": "$HOME/.local/share/virtualenvs/air_quality_bluetooth_le-PO89Jxuj/bin/python"
}
```

It's also useful to edit User Settings and add `editor.formatOnSave` to automatically format your code to the PEP8 style guide.

```json
{
    "editor.formatOnSave": true
}
```

VS Code may prompt you to install `pylint` and `autopep8`.

Go to Debugger -> Add Configuration -> `launch.json`, then add the following entry. You can modify the arguments as needed, and/or make additional launch configurations.

```json
{
    "name": "Python AQI (macOS)",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/cli.py",
    "args": [
        "-p",
        "/dev/tty.wchusbserial1420"
    ]
},
```

[Remote debugging](https://benoitpatra.com/2017/11/27/remote-debugging-python-with-vscode/) is a bit more complicated. 

On your Raspberry Pi you'll need `libdbus` installed to install the Python dependencies.

```bash
$ sudo apt-get install libdbus-1-dev
```


## Dependencies

* [sds011_particle_sensor](https://gitlab.com/frankrich/sds011_particle_sensor) - Control your Nova Fitness SDS011 (PM2.5, PM10) air-particle sensor via python. Control duty cycle, passive mode, sleep mode, get firmware version etc. on windows. linux and even raspberry pi.
* [python-bluezero](https://github.com/ukBaz/python-bluezero) - A simple Python interface to BlueZ stack - Bluetooth LE on Linux

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.

## License

GPLv3