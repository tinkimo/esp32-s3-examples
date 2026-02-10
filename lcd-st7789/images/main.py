from machine import Pin, SPI, PWM
import st7789py as st7789
import utime

# =========================================
# Pins (ESP32-S3)
# =========================================
LCD_DC   = 8
LCD_BL   = 9
LCD_RST  = 12
LCD_SCK  = 13
LCD_MOSI = 11
LCD_BRIGHTNESS = 65535

# =========================================
# Display size
# =========================================
SCREEN_W = 240
SCREEN_H = 240

# =========================================
# Your logo size (set these to match your image)
# Example: if your logo is 120x120, set LOGO_W=120, LOGO_H=120
# =========================================
LOGO_W = 240
LOGO_H = 240
LOGO_FILE = "logo.rgb565"   # converted from logo.png

# =========================================
# SPI setup
# =========================================
spi = SPI(
    1,
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
    SCREEN_W,
    SCREEN_H,
    reset=rst,
    dc=dc,
    cs=None,
    backlight=None,
    rotation=0,
    color_order=st7789.BGR,
)

def show_rgb565(filename, img_w, img_h, x, y):
    # Each pixel is 2 bytes in RGB565
    expected_bytes = img_w * img_h * 2

    with open(filename, "rb") as f:
        buf = f.read()

    if len(buf) != expected_bytes:
        raise ValueError(
            "Image size mismatch. "
            "Expected {} bytes for {}x{} RGB565, got {} bytes.".format(
                expected_bytes, img_w, img_h, len(buf)
            )
        )

    # Draw the image to the screen
    tft.blit_buffer(buf, x, y, img_w, img_h)

# --------------------
# Display logo demo
# --------------------
tft.fill(st7789.BLACK)

# Centre the logo
x = (SCREEN_W - LOGO_W) // 2
y = (SCREEN_H - LOGO_H) // 2

show_rgb565(LOGO_FILE, LOGO_W, LOGO_H, x, y)

while True:
    utime.sleep_ms(50)

