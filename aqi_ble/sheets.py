import gspread
from oauth2client.service_account import ServiceAccountCredentials
from .sensor import SensorReading
from typing import Optional, List, Tuple
import sys
# Backport of Python 3.7 dataclasses. Remove when Python 3.7 is released!
from dataclasses import dataclass
from enum import Enum, auto


@dataclass
class Row:
    @dataclass
    class Cell:
        class Type(Enum):
            name = "Name"
            latitude = "Latitude"
            longitude = "Longitude"
            elevation = "Elevation"
            timestamp = "Timestamp"
            pm2_5 = "PM2.5"
            pm10 = "PM10"
        type: Type
        value: str

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
        columns: [Row.Cell] = [
            Row.Cell(type=Row.Cell.Type.timestamp,
                     value=reading.timestamp_str()),
            Row.Cell(type=Row.Cell.Type.pm2_5, value=str(reading.pm2_5)),
            Row.Cell(type=Row.Cell.Type.pm10, value=str(reading.pm10)),
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
            # This doesn't seem to work...
            # self.worksheet = self.spreadsheet.add_worksheet(title=maya.now().rfc2822(), rows="100", cols="20")
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
        self.worksheet.insert_row(index=2, values=values)
