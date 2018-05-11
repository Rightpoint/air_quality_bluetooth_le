# -*- coding: utf-8 -*-

"""Console script for aqi_ble."""
import sys
import click
from sensor import Sensor, SensorReading

@click.command()
@click.option('-p', '--path', required=True, type=click.Path(exists=True), help='Path to USB TTY sensor device. e.g. /dev/ttyUSB0')
def main(path: str):
    """Console script for aqi_ble."""
    click.echo(f"Opening sensor at path: {path}")
    sensor = Sensor(path=path)
    while True:
        reading = sensor.get_reading()
        if reading is not None:
            print(f"{reading.as_string()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
