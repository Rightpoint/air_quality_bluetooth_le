# -*- coding: utf-8 -*-
from .sheets import Spreadsheet
from .sensor import Sensor, SensorReading, Location
from typing import Optional, Tuple


class Manager:
    sensor: Sensor
    sheet: Optional[Spreadsheet]

    def __init__(self,
                 path: str,
                 json_keyfile: Optional[str],
                 sheet_url: Optional[str],
                 coordinate: Optional[Tuple[float, float]],
                 elevation: Optional[float],
                 name: Optional[str]):
        location: Optional[Location] = None
        if len(coordinate) == 2:
            location = Location(
                latitude=coordinate[0], longitude=coordinate[1], elevation=elevation)
        self.sensor = Sensor(path=path, location=location, name=name)
        self.sheet: Optional[Spreadsheet] = None
        if json_keyfile is not None and sheet_url is not None:
            self.sheet = Spreadsheet(
                json_keyfile=json_keyfile, sheet_url=sheet_url)

    def reset_sensor(self):
        self.sensor.reset()

    def get_reading(self):
        try:
            reading = self.sensor.get_reading()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            print(f"Could not read from sensor: {e}")
        if reading is None:
            return
        print(f"{reading}")
        if self.sheet is not None:
            try:
                self.sheet.post_reading(reading)
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                print(f"Could not post to spreadsheet: {e}")
