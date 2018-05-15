# Standard modules
import os
import dbus
import struct
try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject
import sys
import random
import time

# Bluezero modules
from bluezero import constants
from bluezero import adapter
from bluezero import advertisement
from bluezero import localGATT
from bluezero import GATT
from .sensor import SensorReading

# constants
AQI_PM_SRVC = '22341000-1234-1234-1234-123456789abc'
PM_2_5_CHRC = '2A6E'
PM_10_CHRC = '2A6F'
PM_2_5_FMT_DSCP = '2904'
PM_10_FMT_DSCP = '2905'


def get_pm_readings():
    readings = []
    i_fake_pm25 = random.randrange(100, 53100, 10)
    pm25 = float(i_fake_pm25)/100
    i_fake_pm10 = i_fake_pm25 + 4000
    pm10 = float(i_fake_pm10)/100
    print('Fake Values - PM 2.5: ', pm25, 'PM 10: ', pm10)
    readings.append(pm25)
    readings.append(pm10)
    time.sleep(2)

    return readings


def hex_bytes_from_float(value):
    answer = []
    ba_little_indian = bytearray(struct.pack("f", value))
    ba_big_indian = ba_little_indian[::-1]
    for bytes in ba_big_indian:
        answer.append(dbus.Byte(bytes))

    return answer


class AQIChrc(localGATT.Characteristic):
    def __init__(self, id: int, uuid: str, service: localGATT.Service, initial_value, name: str):
        localGATT.Characteristic.__init__(self,
                                          id,
                                          uuid,
                                          service,
                                          initial_value,
                                          False,
                                          ['read', 'notify'])
        self.name = name
        self.id = id
        self.uuid = uuid

    @property
    def get_reading(self):
        return self._get_reading

    @get_reading.setter
    def get_reading(self, value):
        self._get_reading = value

    def pm_readings_cb(self):
        get_reading_function = self.get_reading
        reading = get_reading_function()
        value = self.parse_reading(reading)
        return self.set_chrc_value(value)

    def parse_reading(self, reading: SensorReading):
        if self.uuid == PM_2_5_CHRC:
            return reading.pm2_5
        elif self.uuid == PM_10_CHRC:
            return reading.pm10
        else:
            return 0.0

    def set_chrc_value(self, new_value: float):
        print('Updating value',
              new_value,
              self.props[constants.GATT_CHRC_IFACE]['Notifying'])
        self.props[constants.GATT_CHRC_IFACE]['Value'] = new_value

        self.PropertiesChanged(constants.GATT_CHRC_IFACE,
                               {'Value': dbus.Array(
                                   hex_bytes_from_float(new_value))},
                               [])
        return self.props[constants.GATT_CHRC_IFACE]['Notifying']

    def _update_pm_values(self):
        if not self.props[constants.GATT_CHRC_IFACE]['Notifying']:
            return

        print('Starting timer event')
        GObject.timeout_add(500, self.pm_readings_cb)

    def ReadValue(self, options):
        return dbus.Array(
            hex_bytes_from_float(
                self.props[constants.GATT_CHRC_IFACE]['Value'])
        )

    def StartNotify(self):
        if self.props[constants.GATT_CHRC_IFACE]['Notifying']:
            print('Already notifying, nothing to do')
            return
        print('Notifying on')
        self.props[constants.GATT_CHRC_IFACE]['Notifying'] = True
        self._update_pm_values()

    def StopNotify(self):
        if not self.props[constants.GATT_CHRC_IFACE]['Notifying']:
            print('Not notifying, nothing to do')
            return

        print('Notifying off')
        self.props[constants.GATT_CHRC_IFACE]['Notifying'] = False
        self._update_pm_values()


class BLE_Peripheral:
    def __init__(self):
        self.bus = dbus.SystemBus()
        self.app = localGATT.Application()
        self.srv = localGATT.Service(1, AQI_PM_SRVC, True)

        self.pm_2_5_charc = AQIChrc(
            1,
            PM_2_5_CHRC,
            self.srv,
            0.0,
            'PM 2.5')
        self.pm_2_5_charc.service = self.srv.path
        self.pm_10_charc = AQIChrc(
            2,
            PM_10_CHRC,
            self.srv,
            0.0,
            'PM 10')
        self.pm_10_charc.service = self.srv.path

        pm_2_5_format_value = dbus.Array([dbus.Byte(0x0E),
                                          dbus.Byte(0xFE),
                                          dbus.Byte(0x2F),
                                          dbus.Byte(0x27),
                                          dbus.Byte(0x01),
                                          dbus.Byte(0x00),
                                          dbus.Byte(0x00)])

        pm_10_format_value = dbus.Array([dbus.Byte(0x0E),
                                         dbus.Byte(0xFE),
                                         dbus.Byte(0x2F),
                                         dbus.Byte(0x27),
                                         dbus.Byte(0x01),
                                         dbus.Byte(0x00),
                                         dbus.Byte(0x00)])

        self.pm_2_5_format = localGATT.Descriptor(4,
                                                  PM_2_5_FMT_DSCP,
                                                  self.pm_2_5_charc,
                                                  pm_2_5_format_value,
                                                  ['read'])

        self.pm_10_format = localGATT.Descriptor(5,
                                                 PM_10_FMT_DSCP,
                                                 self.pm_10_charc,
                                                 pm_10_format_value,
                                                 ['read'])

        self.app.add_managed_object(self.srv)
        self.app.add_managed_object(self.pm_2_5_charc)
        self.app.add_managed_object(self.pm_2_5_format)
        self.app.add_managed_object(self.pm_10_charc)
        self.app.add_managed_object(self.pm_10_format)

        self.srv_mng = GATT.GattManager(adapter.list_adapters()[0])
        self.srv_mng.register_application(self.app, {})

        self.dongle = adapter.Adapter(adapter.list_adapters()[0])
        advert = advertisement.Advertisement(1, 'peripheral')

        advert.service_UUIDs = [AQI_PM_SRVC]
        if not self.dongle.powered:
            self.dongle.powered = True
        ad_manager = advertisement.AdvertisingManager(self.dongle.address)
        ad_manager.register_advertisement(advert, {})

    @property
    def get_reading(self):
        return self._get_reading

    @get_reading.setter
    def get_reading(self, value):
        self._get_reading = value

    def add_call_back(self, callback):
        self.pm_2_5_charc.PropertiesChanged = callback
        self.pm_10_charc.PropertiesChanged = callback

    def start_bt(self):
        self.app.start()
        print('Completed app.start_bt()')
