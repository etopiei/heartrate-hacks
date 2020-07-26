import gatt, struct

manager = gatt.DeviceManager(adapter_name='hci0')

class AnyDevice(gatt.Device):
    def services_resolved(self):
        super().services_resolved()

        heart_rate_service = next(
            s for s in self.services
            if s.uuid == '0000180d-0000-1000-8000-00805f9b34fb')

        hr_measurement_characteristic = next(
            c for c in heart_rate_service.characteristics
            if c.uuid == '00002a37-0000-1000-8000-00805f9b34fb')

        hr_measurement_characteristic.enable_notifications()

    def characteristic_enable_notification_succeeded(self, args):
        print("We have subscribed to HR")

    def characteristic_value_updated(self, characteristic, value):
        # We only want the second byte
        secondToEnd = value[1:]
        secondByte = secondToEnd[0:1]
        hr_value = struct.unpack('B', secondByte)
        hr_str = str(hr_value)[1:].split(",")[0]
        print("\033c", end="")
        print("❤️", " ", hr_str)

device = AnyDevice(mac_address='EB:48:6B:02:72:8B', manager=manager)
device.connect()

manager.run()
