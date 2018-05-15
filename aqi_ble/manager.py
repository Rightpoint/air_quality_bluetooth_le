# -*- coding: utf-8 -*-
from .sheets import Spreadsheet
from .sensor import Sensor, SensorReading, Location
from typing import Optional, Tuple
import sys

try:
    from .ble import BLE_Peripheral
except ImportError:
    class BLE_Peripheral:
        def __init__(self):
            print("Bluetooth support not available!", file=sys.stderr)


class Manager:
    sensor: Sensor
    sheet: Optional[Spreadsheet]
    peripheral: Optional[BLE_Peripheral]

    def __init__(self,
                 path: str,
                 json_keyfile: Optional[str],
                 sheet_url: Optional[str],
                 coordinate: Optional[Tuple[float, float]],
                 elevation: Optional[float],
                 name: Optional[str],
                 enable_bluetooth: Optional[bool]):
        location: Optional[Location] = None
        if len(coordinate) == 2:
            location = Location(
                latitude=coordinate[0], longitude=coordinate[1], elevation=elevation)
        self.sensor = Sensor(path=path, location=location, name=name)
        self.sheet: Optional[Spreadsheet] = None
        if json_keyfile is not None and sheet_url is not None:
            self.sheet = Spreadsheet(
                json_keyfile=json_keyfile, sheet_url=sheet_url)
        if enable_bluetooth is True:
            self.peripheral = BLE_Peripheral()

    def reset_sensor(self):
        self.sensor.reset()

    def get_reading(self):
        try:
            reading = self.sensor.get_reading()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            print(f"Could not read from sensor: {e}", file=sys.stderr)
        if reading is None:
            return
        print(f"{reading}")
        if self.sheet is not None:
            try:
                self.sheet.post_reading(reading)
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                print(f"Could not post to spreadsheet: {e}", file=sys.stderr)
