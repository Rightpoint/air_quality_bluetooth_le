# -*- coding: utf-8 -*-

"""Main module."""

from sds011 import SDS011
from typing import Optional
import maya


class Location:
    def __init__(self, latitude: float, longitude: float, elevation: Optional[float] = None):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation

    def __str__(self) -> str:
        string = f"({self.latitude}, {self.longitude})\t"
        if self.elevation is not None:
            string = string + f" @ {self.elevation}m\t"
        return string

class SensorReading:

    def __init__(self, pm2_5: float, pm10: float, sensor_name: Optional[str] = None, location: Optional[Location] = None):
        self.sensor_name = sensor_name
        self.location = location
        self.pm2_5 = pm2_5
        self.pm10 = pm10
        self.timestamp = maya.now()

    def get_timestamp(self) -> str:
        return self.timestamp.rfc2822()

    def __str__(self) -> str:
        string = ""
        if self.sensor_name is not None:
            string = string + f"{self.sensor_name} - "
        string = string + f"PM2.5: {self.pm2_5}\tPM10: {self.pm10}\t{self.get_timestamp()}\t"
        if self.location is not None:
            string = string + str(self.location)
        return string


class Sensor:

    def __init__(self, path: str, name: Optional[str] = None, location: Optional[Location] = None):
        self.name = name
        self.location = location
        unit_of_measure = SDS011.UnitsOfMeasure.MassConcentrationEuropean
        timeout = 2  # timeout on serial line read
        self.sensor = SDS011(path, timeout=timeout, unit_of_measure=unit_of_measure)

    def __str__(self) -> str:
        return f"Sensor Name: {self.name}\tLocation: {self.location}"

    def get_reading(self) -> Optional[SensorReading]:
        values = self.sensor.get_values()
        if values is None:
            return None
        reading = SensorReading(pm2_5=values[0], pm10=values[1], sensor_name=self.name, location=self.location)
        return reading
