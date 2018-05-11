Air Quality Bluetooth LE
========================

[![image](https://img.shields.io/pypi/v/aqi_ble.svg)](https://pypi.python.org/pypi/aqi_ble)

[![image](https://img.shields.io/travis/Raizlabs/aqi_ble.svg)](https://travis-ci.org/Raizlabs/aqi_ble)

[![Documentation Status](https://readthedocs.org/projects/aqi-ble/badge/?version=latest)](https://aqi-ble.readthedocs.io/en/latest/?badge=latest)

Bluetooth Low Energy interface for SDS011 APM2.5 air quality sensor

## Features

-   TODO

## Installation

### Install Pipenv

Install [Python 3](https://www.python.org/) and [Pipenv](https://github.com/pypa/pipenv) to manage Python dependencies.

#### macOS

```
$ brew install python3
$ pip3 install -U pipenv
```

#### Linux

```
$ sudo apt-get install python3-pip
$ pip3 install -U pipenv
```

### Setup

Clone the repo and run `pipenv` to install the dependencies:

```
$ git clone https://github.com/Raizlabs/air_quality_bluetooth_le.git
$ cd air_quality_bluetooth_le/
$ pipenv install
```

To run the tests use `pipenv shell` to activate the virtual environment:

```
$ pipenv shell
$ make test
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