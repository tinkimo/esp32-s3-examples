from machine import Pin, SPI, PWM
import st7789py as st7789
import vga1_8x8 as font
import utime

# =========================================
# Pins (confirmed valid on your ESP32-S3)
# =========================================
LCD_DC   = 8
LCD_BL   = 9
LCD_RST  = 12
LCD_SCK  = 13
LCD_MOSI = 11
LCD_BRIGHTNESS=65535

# =========================================
# SPI setup
# =========================================
spi = SPI(
    1,                 # <-- change from 2 to 1
    baudrate=40_000_000,
    polarity=1,
    phase=1,
    sck=Pin(LCD_SCK),
    mosi=Pin(LCD_MOSI),
)

dc  = Pin(LCD_DC, Pin.OUT)
rst = Pin(LCD_RST, Pin.OUT)

# Backlight PWM (optional dimming)
bl_pwm = PWM(Pin(LCD_BL), freq=20000, duty_u16=LCD_BRIGHTNESS)

tft = st7789.ST7789(
    spi,
    240,
    240,
    reset=rst,
    dc=dc,
    cs=None,         
    backlight=None,   
    rotation=0,
    color_order=st7789.BGR,
)



# --------------------
# Drawing demo
# --------------------
tft.fill(st7789.BLACK)

# Filled rectangle
tft.fill_rect(20, 20, 80, 40, st7789.RED)

# Rectangle outline
tft.rect(120, 20, 80, 40, st7789.GREEN)

# Horizontal line
tft.hline(20, 80, 200, st7789.YELLOW)

# Vertical line
tft.vline(120, 80, 100, st7789.CYAN)

# Text
tft.text(font, "Drawing With Tinkimo!", 40, 210, st7789.WHITE)

while True:
    utime.sleep_ms(10)  
