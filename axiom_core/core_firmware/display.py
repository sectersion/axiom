import time
from machine import Pin, SPI
from ili9341 import Display, color565

class BruceDisplay:
    # Standard 16-bit Colors
    WHITE = color565(255, 255, 255)
    BLACK = color565(0, 0, 0)
    GREEN = color565(0, 255, 0)
    RED   = color565(255, 0, 0)
    BLUE  = color565(0, 0, 255)
    GREY  = color565(100, 100, 100)

    def __init__(self, spi, cs=15, dc=2, rst=4):
        """
        Abstraction for ILI9341. 
        Pins default to common ESP32 devkit layouts.
        """
        self.display = Display(spi, dc=Pin(dc), cs=Pin(cs), rst=Pin(rst))
        self.display.clear(self.BLACK)
        self.current_line = 0
        self.max_lines = 12
        self.line_height = 20

    def draw_header(self, title="BRUCE NRF"):
        """Draws a top status bar."""
        self.display.fill_rectangle(0, 0, 240, 25, self.BLUE)
        self.display.draw_text(5, 5, title, self.WHITE)
        self.display.draw_hline(0, 26, 240, self.WHITE)

    def log(self, message, color=WHITE):
        """Scroll-style logging for the screen."""
        if self.current_line >= self.max_lines:
            # Clear log area and restart if full (simplified)
            self.display.fill_rectangle(0, 30, 240, 290, self.BLACK)
            self.current_line = 0
        
        y_pos = 30 + (self.current_line * self.line_height)
        self.display.draw_text(5, y_pos, f"> {message}", color)
        self.current_line += 1

    def draw_hit_list(self, hits):
        """Renders a list of found addresses."""
        self.display.fill_rectangle(0, 30, 240, 290, self.BLACK)
        self.display.draw_text(5, 30, "FOUND DEVICES:", self.GREEN)
        for i, hit in enumerate(hits[:10]): # Show first 10
            self.display.draw_text(10, 55 + (i * 20), f"[{i}] {hit}", self.WHITE)

    def show_status(self, nrf_a_status, nrf_b_status):
        """Shows status of both chips at the bottom."""
        self.display.fill_rectangle(0, 300, 240, 20, self.GREY)
        status_str = f"A: {nrf_a_status} | B: {nrf_b_status}"
        self.display.draw_text(5, 302, status_str, self.BLACK)