import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sensor import SensorReading
from typing import Optional, List, Any
import sys
# Backport of Python 3.7 dataclasses. Remove when Python 3.7 is released!
from dataclasses import dataclass


class Spreadsheet:
    spreadsheet: Optional[gspread.Spreadsheet] = None
    worksheet: Optional[gspread.Worksheet] = None
    heading: Optional[List[str]] = None

    def __init__(self, json_keyfile: str, sheet_url: str):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
        gc = gspread.authorize(credentials)
        try:
            self.spreadsheet = gc.open_by_url(sheet_url)
            self.worksheet = self.spreadsheet.sheet1
            # This doesn't seem to work...
            # self.worksheet = self.spreadsheet.add_worksheet(title=maya.now().rfc2822(), rows="100", cols="20")
        except gspread.SpreadsheetNotFound as err:
            print(f"Spreadsheet not found: {err}", file=sys.stderr)

    def post_reading(self, reading: SensorReading):
        heading: List[str] = ['Timestamp', 'PM2.5', 'PM10']
        row: List[str] = [reading.get_timestamp(), reading.pm2_5, reading.pm10]
        if reading.sensor_name is not None:
            heading.append('Name')
            row.append(reading.sensor_name)
        if reading.location is not None:
            heading.append('Latitude')
            heading.append('Longitude')
            row.append(reading.location.latitude)
            row.append(reading.location.longitude)
            if reading.location.elevation is not None:
                heading.append('Elevation (meters)')
                row.append(reading.location.elevation)
        if self.heading is None:
            self.heading = heading
            self.worksheet.insert_row(heading)
        self.worksheet.append_row(row)

