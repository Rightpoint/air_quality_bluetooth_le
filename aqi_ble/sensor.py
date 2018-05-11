# -*- coding: utf-8 -*-

"""Main module."""

from sds011 import SDS011
from typing import Optional


class SensorReading:

    def __init__(self, pm_2_5: float, pm_10: float):
        self.pm_2_5 = pm_2_5
        self.pm_10 = pm_10

    def as_string(self) -> str:
        return f"PM2.5: {self.pm_2_5}\tPM10: {self.pm_10}"


class Sensor:

    def __init__(self, path: str):
        unit_of_measure = SDS011.UnitsOfMeasure.MassConcentrationEuropean
        timeout = 2  # timeout on serial line read
        self.sensor = SDS011(path, timeout=timeout, unit_of_measure=unit_of_measure)

    def get_reading(self) -> Optional[SensorReading]:
        values = self.sensor.get_values()
        if values is None:
            return None
        reading = SensorReading(pm_2_5=values[0], pm_10=values[1])
        return reading
