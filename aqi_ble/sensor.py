# -*- coding: utf-8 -*-

"""Main module."""

from sds011 import SDS011
from typing import Optional, List
import maya
from maya import MayaDT
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
    sensor_name: Optional[str] = None
    location: Optional[Location] = None
    timestamp: MayaDT = maya.now()

    def get_timestamp(self) -> str:
        return self.timestamp.rfc2822()

    def __str__(self) -> str:
        string: str = ""
        if self.sensor_name is not None:
            string = string + f"{self.sensor_name} - "
        string = string + f"PM2.5: {self.pm2_5}\tPM10: {self.pm10}\t{self.get_timestamp()}\t"
        if self.location is not None:
            string = string + str(self.location)
        return string

    def get_heading(self) -> List[str]:
        heading: List[str] = ['Timestamp', 'PM2.5', 'PM10']
        if self.sensor_name is not None:
            heading.append('Name')
        if self.location is not None:
            heading.append('Latitude')
            heading.append('Longitude')
            if self.location.elevation is not None:
                heading.append('Elevation (meters)')

    def get_row(self) -> List[str]:
        row: List[str] = [self.get_timestamp(), self.pm2_5, self.pm10]
        if self.sensor_name is not None:
            row.append(self.sensor_name)
        if self.location is not None:
            row.append(str(self.location.latitude))
            row.append(str(self.location.longitude))
            if self.location.elevation is not None:
                row.append(str(self.location.elevation))


class Sensor:
    path: str
    name: Optional[str] = None
    location: Optional[Location] = None

    def __init__(self,
                 path: str,
                 name: Optional[str] = None,
                 location: Optional[Location] = None):
        self.name = name
        self.location = location
        unit_of_measure = SDS011.UnitsOfMeasure.MassConcentrationEuropean
        timeout: int = 2  # timeout on serial line read
        self.sensor = SDS011(path, timeout=timeout, unit_of_measure=unit_of_measure)

    def __str__(self) -> str:
        return f"Sensor Name: {self.name}\tLocation: {self.location}"

    def get_reading(self) -> Optional[SensorReading]:
        values = self.sensor.get_values()
        if values is None:
            return None
        return SensorReading(pm2_5=values[1], pm10=values[0], sensor_name=self.name, location=self.location)
