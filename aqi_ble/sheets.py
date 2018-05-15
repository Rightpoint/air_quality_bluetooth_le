#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from .sensor import SensorReading
from typing import Optional, List, Tuple, Any
import sys
# Backport of Python 3.7 dataclasses. Remove when Python 3.7 is released!
from dataclasses import dataclass
from enum import Enum, auto
import datetime
import pytz


@dataclass
class Row:
    @dataclass
    class Cell:
        class Type(Enum):
            name = "Name"
            latitude = "Latitude"
            longitude = "Longitude"
            elevation = "Elevation (m)"
            timestamp = "Timestamp"
            pm2_5 = "PM2.5"
            pm10 = "PM10"
        type: Type
        value: Any

    columns: [Cell]

    def get_heading(self) -> [str]:
        heading: [str] = []
        for column in self.columns:
            heading.append(column.type.value)
        return heading

    def get_values(self) -> [str]:
        values: [str] = []
        for column in self.columns:
            values.append(column.value)
        return values

    @classmethod
    def from_reading(cls, reading: SensorReading):
        #epoch = datetime.datetime(1899, 12, 30).replace(tzinfo=pytz.utc)
        #timestamp = (reading.timestamp - epoch)
        timestamp = reading.timestamp_str()
        columns: [Row.Cell] = [
            Row.Cell(type=Row.Cell.Type.timestamp,
                     value=timestamp),
            Row.Cell(type=Row.Cell.Type.pm2_5, value=reading.pm2_5),
            Row.Cell(type=Row.Cell.Type.pm10, value=reading.pm10),
            Row.Cell(type=Row.Cell.Type.name, value=reading.sensor_name),
            Row.Cell(type=Row.Cell.Type.latitude,
                     value=reading.location.latitude),
            Row.Cell(type=Row.Cell.Type.longitude,
                     value=reading.location.longitude),
            Row.Cell(type=Row.Cell.Type.elevation,
                     value=reading.location.elevation),
        ]
        return Row(columns=columns)


class Spreadsheet:
    spreadsheet: Optional[gspread.Spreadsheet] = None
    worksheet: Optional[gspread.Worksheet] = None
    heading: Optional[List[str]] = None

    def __init__(self,
                 json_keyfile: str,
                 sheet_url: str):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            json_keyfile, scope)
        gc = gspread.authorize(credentials)
        try:
            self.spreadsheet = gc.open_by_url(sheet_url)
            self.worksheet = self.spreadsheet.sheet1
            # now = datetime.datetime.now(tz=pytz.utc)
            # title = now.strftime("%m/%d/%Y %H:%M:%S")
            # This doesn't seem to work...
            # self.worksheet = self.spreadsheet.add_worksheet(
            #    title=title, rows=len(Row.Cell.Type), cols="100")
        except gspread.SpreadsheetNotFound as err:
            print(f"Spreadsheet not found: {err}", file=sys.stderr)

    def post_reading(self, reading: SensorReading):
        if self.worksheet is None:
            return
        row: Row = Row.from_reading(reading)
        if self.heading is None:
            self.heading = row.get_heading()
            self.worksheet.insert_row(index=1, values=self.heading)
        values = row.get_values()
        self.worksheet.append_row(values)
