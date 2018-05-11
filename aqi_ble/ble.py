import objc
import Cocoa
from CoreBluetooth import CBPeripheralManager, CBUUID, CBMutableService, CBService


class Peripheral (Cocoa.NSObject):
    manager: CBPeripheralManager = objc.ivar()
    service: CBService = objc.ivar()

    def init(self):
        self = objc.super(Peripheral, self).init()
        if self is None:
            return None
        self.manager = CBPeripheralManager.alloc().init()
        self.manager.setDelegate_(self)
        uuid = CBUUID.UUIDWithString_("88C44C08-DB0B-407E-A17B-8E0F61ADA78B")

        self.service = CBMutableService.alloc().initWithType_primary_(uuid, True)
        self.manager.addService_(self.service)

    def peripheralManager_didUpdateState_(self,
            peripheral: CBPeripheralManager, sender):
        print(f"Did update state {peripheral}")

    def peripheralManager_didAddService_error_(self, peripheral, service, error):
        print(f"Did add service {service}")
