#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Console script for aqi_ble."""
import sys
import click
from .sheets import Spreadsheet
from .sensor import Sensor, SensorReading, Location
from .manager import Manager
from typing import Optional, Tuple
import time


@click.command()
@click.option('-p', '--path', required=True, type=click.Path(exists=True), help='Path to SDS011 USB TTY sensor device. e.g. /dev/ttyUSB0')
@click.option('--json_keyfile', type=click.Path(exists=True), help='Path to Google OAuth JSON Keyfile')
@click.option('--sheet_url', help='Google Sheets URL')
@click.option('--coordinate', nargs=2, type=float, help='GPS Coordinate (Latitude Longitude) e.g. 37.8066073985003 -122.27042233335567')
@click.option('--elevation', type=float, help='Sensor Elevation in Meters e.g. 40')
@click.option('--name', help='Sensor Name e.g. Bedroom')
@click.option('--remote_debug_secret', help='Remote Debugging attachment secret e.g. my_secret')
@click.option('--remote_debug_address', help='Remote Debugging IP e.g. 0.0.0.0')
@click.option('--remote_debug_port', type=int, help='Remote Debugging port e.g. 3000')
@click.option('--remote_debug_wait', type=bool, help='Wait for Remote Debugger to attach')
def main(path: str,
         json_keyfile: Optional[str],
         sheet_url: Optional[str],
         coordinate: Optional[Tuple[float, float]],
         elevation: Optional[float],
         name: Optional[str],
         remote_debug_secret: Optional[str],
         remote_debug_address: Optional[str],
         remote_debug_port: Optional[int],
         remote_debug_wait: Optional[bool],
         ):
    if remote_debug_secret is not None and remote_debug_address is not None:
        click.echo(f"Enabling remote debugging: {remote_debug_address}")
        import ptvsd
        ptvsd.enable_attach(remote_debug_secret,
                            address=(remote_debug_address, remote_debug_port))
        if remote_debug_wait:
            ptvsd.wait_for_attach()
    click.echo(f"Opening sensor at path: {path}")
    manager = Manager(path=path, json_keyfile=json_keyfile, sheet_url=sheet_url,
                      coordinate=coordinate, elevation=elevation, name=name)
    while True:
        manager.get_reading()
        time.sleep(2)
    return 0
