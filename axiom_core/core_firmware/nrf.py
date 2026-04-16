from machine import Pin, SPI
from nrf24l01 import NRF24L01
import time
import struct


class BruceNRF:
    def __init__(self, spi, ce_pin, csn_pin, name="NRF"):
        self.nrf = NRF24L01(spi, Pin(ce_pin), Pin(csn_pin), payload_size=32)
        self.name = name

    def set_mode(self, mode="RX", channel=76):
        self.nrf.stop_listening()
        self.nrf.set_channel(channel)
        if mode == "RX":
            self.nrf.start_listening()
        return f"{self.name} set to {mode} on CH {channel}"

    def jam(self, duration=5):
        self.nrf.stop_listening()
        self.nrf._reg_write(0x06, 0x90) 
        time.sleep(duration)
        self.nrf._reg_write(0x06, 0x00) # Disable

    def replay_packet(self, raw_data):
        self.nrf.stop_listening()
        self.nrf.send(raw_data)
        self.nrf.start_listening()

    def sniff_loop(self, callback, duration=10):
        self.nrf.start_listening()
        start = time.time()
        while time.time() - start < duration:
            if self.nrf.any():
                callback(self.nrf.recv())
        self.nrf.stop_listening()

    def send_hid_sequence(self, address, sequence):
        self.nrf.open_tx_pipe(address)
        for char in sequence:
            packet = struct.pack("<BBBB", 0x00, 0xC1, ord(char), 0x00)
            self.nrf.send(packet)
            time.sleep_ms(20)

    def get_signal_strength(self):
        return self.nrf._reg_read(0x09) & 0x01