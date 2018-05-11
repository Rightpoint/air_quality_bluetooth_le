# -*- coding: utf-8 -*-

"""Console script for aqi_ble."""
import sys
import click
from sheets import Spreadsheet
from sensor import Sensor, SensorReading, Location
from typing import Optional

@click.command()
@click.option('-p', '--path', required=True, type=click.Path(exists=True), help='Path to USB TTY sensor device. e.g. /dev/ttyUSB0')
@click.option('--json_keyfile', type=click.Path(exists=True), help='Path to Google OAuth JSON Keyfile')
@click.option('--sheet_url', help='Google Sheets URL')
@click.option('--coordinate', type=(float, float), help='GPS Coordinate (Latitude Longitude) e.g. 37.8066073985003 -122.27042233335567')
@click.option('--elevation', type=float, help='Sensor Elevation in Meters e.g. 40')
@click.option('--name', help='Sensor Name e.g. Bedroom')
def main(path: str, json_keyfile: Optional[str], sheet_url: Optional[str], coordinate: (float, float), elevation: Optional[float], name: Optional[str]):
    click.echo(f"Opening sensor at path: {path}")
    location: Optional[Location] = None
    if coordinate is not None:
        location = Location(latitude=coordinate[0], longitude=coordinate[1], elevation=elevation)
    sensor = Sensor(path=path, location=location, name=name)
    sheet: Optional[Spreadsheet] = None
    if json_keyfile is not None and sheet_url is not None:
        sheet = Spreadsheet(json_keyfile=json_keyfile, sheet_url=sheet_url)
    while True:
        reading = sensor.get_reading()
        if reading is not None:
            print(f"{reading}")
            if sheet is not None:
                sheet.post_reading(reading)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
