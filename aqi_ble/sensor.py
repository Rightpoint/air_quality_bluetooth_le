#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module."""

from .sds011 import SDS011
from typing import Optional, List
import datetime as dt
import pytz
# Backport of Python 3.7 dataclasses. Remove when Python 3.7 is released!
from dataclasses import dataclass


@dataclass
class Location:
    latitude: float
    longitude: float
    # meters
    elevation: Optional[float] = None

    def __str__(self) -> str:
        string = f"({self.latitude}, {self.longitude})\t"
        if self.elevation is not None:
            string = string + f" @ {self.elevation}m\t"
        return string


@dataclass
class SensorReading:
    pm2_5: float
    pm10: float
    sensor_name: str
    timestamp: dt.datetime
    location: Optional[Location] = None

    def timestamp_str(self) -> str:
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self) -> str:
        string: str = f"{self.sensor_name} - "
        string += f"PM2.5: {self.pm2_5}\tPM10: {self.pm10}\t{self.timestamp_str()}\t"
        if self.location is not None:
            string += str(self.location)
        return string


class Sensor:
    name: str = "Sensor"
    location: Optional[Location] = None

    def __init__(self,
                 path: str,
                 name: Optional[str] = None,
                 location: Optional[Location] = None):
        if name is not None:
            self.name = name
        self.location = location
        unit_of_measure = SDS011.UnitsOfMeasure.MassConcentrationEuropean
        timeout: int = 2  # timeout on serial line read
        self.sensor = SDS011(path, timeout=timeout,
                             unit_of_measure=unit_of_measure)

    def __str__(self) -> str:
        return f"Sensor Name: {self.name}\tLocation: {self.location}"

    def get_reading(self) -> Optional[SensorReading]:
        values = self.sensor.get_values()
        if values is None:
            return None
        return SensorReading(pm2_5=values[1],
                             pm10=values[0],
                             sensor_name=self.name,
                             location=self.location,
                             timestamp=dt.datetime.now(tz=pytz.utc))
