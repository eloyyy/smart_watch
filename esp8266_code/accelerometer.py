import ustruct
from machine import SPI, Pin
import shared

# Register constants for the ADXL345 accelerometer
# POWER_CTL = const(0x2D)
# DATA_FORMAT = const(0x31)


cs = Pin(4, Pin.OUT)
spi = SPI(-1, baudrate=500000, polarity=1, phase=1, sck=Pin(5), mosi=Pin(2), miso=Pin(16))

def setup():
    writeA(shared.DATA_FORMAT, 0x01)
    writeA(shared.POWER_CTL, 0x08)

# Write command/value to specified register
def writeA(register, value):
    global cs, vcc, grnd, spi

    # Pack register and value into byte format
    write_val = ustruct.pack('B',value)
    write_reg_val = ustruct.pack('B',register)

    # Pull line low and write to accelerometer
    cs.value(0)
    spi.write(write_reg_val)
    spi.write(write_val)
    cs.value(1)

# Read value from a specified register
def readA():
    import shared
    global cs, vcc, grnd, spi

    # Set the R/W bit high to specify "read" mode
    reg = shared.DATAX0
    reg = 0x80 | reg

    # Set the MB bit high to specify that we want to
    # do multi byte reads.
    reg = reg | 0x40

    # Pack R/W bit + MB bit + register value into byte format
    write_reg_val = ustruct.pack('B',reg)

    # Setup buffers for receiving data from the accelerometer.
    x1 = bytearray(1)
    x2 = bytearray(1)
    y1 = bytearray(1)
    y2 = bytearray(1)
    z1 = bytearray(1)
    z2 = bytearray(1)

    # Read from all 6 accelerometer data registers, one address at a time
    cs.value(0)
    spi.write(write_reg_val)
    spi.readinto(x1)
    spi.readinto(x2)
    spi.readinto(y1)
    spi.readinto(y2)
    spi.readinto(z1)
    spi.readinto(z2)
    cs.value(1)
    
    # Reconstruct the X, Y, Z axis readings from the received data.
    x = (ustruct.unpack('b',x2)[0]<<8) | ustruct.unpack('b',x1)[0]
    y = (ustruct.unpack('b',y2)[0]<<8) | ustruct.unpack('b',y1)[0]
    z = (ustruct.unpack('b',z2)[0]<<8) | ustruct.unpack('b',z1)[0]
    return (x,y,z)