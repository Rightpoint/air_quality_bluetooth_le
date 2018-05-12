import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sensor import SensorReading
from typing import Optional, List
import maya


class Spreadsheet:

    def __init__(self, json_keyfile: str, sheet_url: str):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
        gc = gspread.authorize(credentials)
        self.spreadsheet = gc.open_by_url(sheet_url)
        self.worksheet = self.spreadsheet.sheet1
        # This doesn't seem to work...
        # self.worksheet = self.spreadsheet.add_worksheet(title=maya.now().rfc2822(), rows="100", cols="20")
        self.heading = None

    def post_reading(self, reading: SensorReading):
        heading = ['Timestamp', 'PM2.5', 'PM10']
        row = [reading.get_timestamp(), reading.pm2_5, reading.pm10]
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
