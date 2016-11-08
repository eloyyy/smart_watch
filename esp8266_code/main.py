ESSID2 = "Columbia University"
PASSWORD = ''

import ssd1306b
from machine import I2C, Pin, SPI, PWM, RTC, ADC
import time
import network
from twitter import *
from buttons import *
from accelerometer import *
global cs, vcc, grnd, spi
import shared

cs = Pin(0, Pin.OUT)
spi = SPI(-1, baudrate=500000, polarity=1, phase=1, sck=Pin(5), mosi=Pin(2), miso=Pin(16))
cs.value(0)
cs.value(1)

setup()

# Set up the display
i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306b.SSD1306_I2C(128, 32, i2c)
display.fill(0)

ip_address = do_connect()

# Set buttons
buttonA = Pin(14, Pin.IN, Pin.PULL_UP)
buttonB = Pin(12, Pin.IN, Pin.PULL_UP)
buttonC = Pin(13, Pin.IN, Pin.PULL_UP)

shared.A = 0
shared.B = 0
shared.isHour = True

buttonB.irq(trigger=Pin.IRQ_FALLING, handler=incrementB)
buttonA.irq(trigger=Pin.IRQ_FALLING, handler=incrementA)
buttonC.irq(trigger=Pin.IRQ_FALLING, handler=decrementA)

res = set_time(buttonA, buttonB, buttonC, display, False)
hour = res['hour']
minutes = res['minutes']
seconds = res['seconds']

# Set current time
rtc = RTC()

year = 2016
month = 9
day = 27
weekday = 3
susbecond = 0

rtc.datetime((year, month, day, weekday, hour, minutes, seconds, susbecond))

# Set alarm
current_time = dict()
shared.isAlarm = False

B = 0

# Create the socket
import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

# Start listenning the network
print('listening on', addr)
isTimeSetup = False
display_time = True
is_tweet = False

hour_alarm = None
minutes_alarm = None

times = [0,0]
tweet_ = 'No last tweet'
last_weather = dict()
last_weather['weather'] = 'clouds'

while True:  

    x, y, z = readA()
    print("x:",x,"y:",y,"z:",z)
    path = 'get_data?' + 'x=' + str(x) + '&y=' + str(y) + '&z=' + str(z)
    a = http_get(path, False)

    # Brigthness Adjustment
    adc = ADC(0)
    contrast = int((adc.read()/1023)*255)
    display.contrast(contrast)
    display.show()

    # Reading Voice Control Input
    socket_received = False
    s.settimeout(0)
    try: 
        cl, addr = s.accept()
        received = False
        while not received:
            try:
                data = str(cl.recv(500))
                received = True
            except:
                pass
        print('client connected from', addr)
        print('Read socket response: ')
        socket_received = True
    except OSError: 
        pass

    if socket_received:
        print(data)
        data = data[data.find('text='):]
        data = data.replace("'","")
        data = data.replace("&","")
        data = data[:data.find('-')]
        print('---------')
        print(data)
        print('---------')
        display.fill(0)

        if is_tweet == True:
            tweet_ = data.replace('text=', '')
            if tweet_ != '':
                path = 'tweet?text=' + str(tweet_)
                temp = http_get(path, False)
                is_tweet = False
                # display.fill(0)
                # display.text('Tweet sent !', 10, 10)
                # display.show()
                time.sleep(1)

        if data == 'text=time':
            display_time = True
            display.fill(0)      
            cl.send(bytes('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n', 'utf8'))
            cl.send(bytes('Time is displayed on the watch', 'utf8'))

        elif data == 'text=alarm':
            t1 = time.time()
            temp = times[0]
            times[0] = t1
            times[1] = temp

            # To avoid the double post request done by the Android app
            if times[0] - times[1] > 50:
                display.fill(0)
                shared.isAlarm = True
                shared.A = 0
                shared.B = 0
                res = set_time(buttonA, buttonB, buttonC, display, True)
                hour_alarm = res['hour']
                minutes_alarm = res['minutes']
                display_time = True

        elif data == 'text=send':
            display_time = False
            display.fill(0)
            display.text('Say your tweet !', 10, 10)
            display.show()
            is_tweet = True

        elif data == 'text=before':
            display_time = False
            display.fill(0)
            display.text(tweet_, 10, 0)
            display.text('Weather = ' + str(last_weather['weather']), 10, 10)
            display.show()

        elif data == 'text=weather':
            display_time = False
            display.fill(0)

            # # extract lon and lattitude from Geolocation Data
            path = 'geoloc?ip=' + str(ip_address)
            temp = http_get(path, False)
            temp = temp.split('\n')[-1]
            temp = json.loads(temp)
            lat = float(temp['lat'])
            lon = float(temp['lon'])

            # Weather api call
            path = 'weather?lat=' + str(lat) + '&' + 'lon=' + str(lon)
            temp = http_get(path, False)
            temp = temp.split('\n')[-1]
            temp = json.loads(temp)
            display.fill(0)
            display.text('Temp = ' + str(temp['temp'])[:4], 10, 0)
            display.text('Pressure = ' + str(temp['pressure'])[:5], 10, 10)
            display.text('Weather = ' + str(temp['weather']), 10, 20)
            display.show()
            last_weather = temp
            time.sleep(2)

        else:
            display_time = False
            display.fill(0)
            data = data.replace('text=', '')
            data = data.replace('+', ' ')
            if data != '':
                display.text(data, 10, 10)
                display.show()
                cl.send(bytes('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n', 'utf8'))
                cl.send(bytes('Text sent to the watch !', 'utf8'))
                time.sleep(2)

        cl.close()

    if display_time:
        display.fill(0)
        year = rtc.datetime()[1]
        month = rtc.datetime()[2]
        day = rtc.datetime()[3]
        hour = rtc.datetime()[4]
        minute = rtc.datetime()[5]
        second = rtc.datetime()[6]
        milisecond = rtc.datetime()[7]
        text = str(hour) + ':' + str(minute) + ':' + str(second)
        display.text(text, 10, 10)
        display.show()
        time.sleep(1)

    if hour_alarm != None:
        alarm_var = dict()
        alarm_var['hour'] = hour_alarm
        alarm_var['minute'] = minutes_alarm
        current_time['hour'] = rtc.datetime()[4]
        current_time['minute'] = rtc.datetime()[5]
        alarm(current_time, alarm_var, display)

