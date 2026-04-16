import time

class BruceScanner:
    def __init__(self, nrf_device):
        self.dev = nrf_device
        self.found_devices = []

    def scan_spectrum(self):
        print("Scanning 2.4GHz Spectrum...")
        spectrum = []
        for i in range(126):
            self.dev.nrf.set_channel(i)
            self.dev.nrf.start_listening()
            time.sleep_ms(5)
            # Check Received Power Detector (RPD)
            if self.dev.get_signal_strength():
                spectrum.append("#")
            else:
                spectrum.append(".")
        print("".join(spectrum))

    def find_logitech(self, timeout=30):
        print("Hunting for Logitech/HID devices...")
        # Common Logitech channels
        channels = [5, 8, 11, 23, 26, 32, 41, 65, 71]
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            for ch in channels:
                self.dev.set_mode("RX", channel=ch)
                # Set promo-lite mode
                self.dev.nrf._reg_write(0x03, 0x00) # 2-byte addr
                self.dev.nrf.open_rx_pipe(1, b'\xCD\x00') 
                
                if self.dev.nrf.any():
                    raw = self.dev.nrf.recv()
                    addr = "CD:" + ":".join(["%02X" % b for b in raw[:4]])
                    if addr not in self.found_devices:
                        self.found_devices.append(addr)
                        print(f"[!] Target Found: {addr} on CH {ch}")
        return self.found_devices