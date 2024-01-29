"""
 Piico_info.py

 PiicoDev devices presence tests

 (c) 2024 Murray Taylor

    This program is free software; you can redistribute it and/or
    modify it under the terms of the BSD 3-clause License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    You should have received a copy of the BSD 3-clause License
    along with this program; if not, a copy is available on the web at
    https://https://opensource.org/license/bsd-3-clause/
"""    

from machine import Pin, I2C

_Debug = 0	# can be chucked out, used to print short WIP messages, and to execute the function tests.


class Piico_info(object):
    """
    PiicoDev devices presence tests
    Murray T 20240129   (v 1.4)
    @Murray125532

    the simple tests without this module
    ------------------------------------
    i2c = I2C(id=0)         # PiicoDev chain on i2c channel 0
    connected = i2c.scan()  # whats connected
    print(connected)        # prints decimal list
    for i in connected:     # prints hexadecimal list
        print(i, hex(i))    #  /

    What this module provides
    =========================
    Instantiation
    -------------
        # the default for standard PiicoDev setup
        tests = Piico_info()
    OR
        # for an alternate i2c bus on GPIO6 and GPOI7
        test_altbus = Piico_info(id=1, scl=Pin(7), sda=Pin(6))
    
    Immediately after this you can display what has been detected on the default i2c bus by either
    
        print(tests.connected)
    or
        tests.show_int()

    these print a list of detected i2c ID's in decimal
        [16, 60, 82, 83, 119]
        
    Available functions
    -------------------
        clear()                 - clears the list of connected i2c devices
        rescan()                - clears and rescans the default i2c bus and repopulates the list
        show_int()              - prints the list of connected ID's in DECIMAL detected by the original/most recent scan
        show_hex()              - prints the list of connected ID's in HEXADECIMAL detected by the original/most recent scan
        is_ID_connected(id)     - returns 1 if the ID is in the list, otherwise 0
        how_many_connected()    - returns count of detected ID's
        
        details()               - prints 'human name' of the connected ID's e.g. 'OLED Module' (default is 'what')
            details('what')     - prints 'human name' of the connected ID's e.g. 'OLED Module'       
            details('short')    - prints 'short_name' of the connected ID's e.g. 'SSD1306'
            details('long')     - prints 'long_name' of the connected ID's e.g. 'PiicoDev OLED Module SSD1306'
        *****
        The details() function can also access a user defined dictionary of devices from other manufacturers.
        The user dictionary MUST be in the same format as the internal dictionaries
        
            extern_list: dict = {
                0x53: {		# 16.  0x10
                    'what': 'Ambient Light-UV Sensor',
                    'long_name': 'Adafruit LTR390 Ambient Light-UV Sensor',
                    'short_name': 'LTR390'},
                <nextID>: {    # possible comment
                    'what': 'simple description',
                    'long_name': 'lengthy description',
                    'short_name': 'MFR code'},
            }

        then calling the details() function as below _AFTER_ the user dictionary is defined, will
        display this if the LTR390 is in the connected devices list
        
            details('what', extern_list ) - prints 'human name' of the connected ID's e.g. 'Ambient Light-UV Sensor'       
            details('short', extern_list) - prints 'short_name' of the connected ID's e.g. 'LTR390'
            details('long', extern_list)  - prints 'long_name' of the connected ID's e.g. 'Adafruit LTR390 Ambient Light-UV Sensor'

        what_is(id)             - prints 'human name' of the given ID e.g. 'RGB LED Module' (default is 'what')
            what_is(id, 'what') - prints 'human name' of the given ID e.g. 'RGB LED Module'
            what_is(id, 'short')- prints 'short_name' of the given ID e.g. 'LED'
            what_is(id, 'long') - prints 'long_name' of the given ID e.g. 'PiicoDev 3x RGB LED Module'
            
        show_all()              - prints all 'human names' from the main internal dictonary (default is 'what')
            show_all('what')    - prints all 'human names' from the main internal dictonary
            show_all('short')   - prints all 'short names' from the main internal dictonary
            show_all('long')    - prints all 'long names' from the main internal dictonary
          ** with extra option 'show' also displays similar entries from the conflicts dictionary
            show_all('what', 'show')    - prints all 'human names' from the conflict internal dictonary
            show_all('short', show')    - prints all 'shout names' from the conflict internal dictonary
            show_all('long', 'show')    - prints all 'long names' from the conflict internal dictonary
            
    Address conflicts
    -----------------
    Where appropriate this module will provide information about potential conflicts, since some PiicoDev devices
    do have addresses that could collide. This can be dealt with by setting the module address switch (ASW)
    to a non default setting (if available), OR by programatically changing the device address if possible.
    
    This module only 'knows' about PiicoDev devices, however an external dictionary can be provided by the user.
    
    ** The module CANNOT detect an actual address conflict on a given i2c bus. This is a characteristic of the bus itself.
    
    'Constant' values
    -----------------
    Internally there is a set of constant names for the PiicoDev addresses, both the default address, and
    if available the alternate address that can be selected by changing the address switch (ASW)
    (at this time only one alternate is provided)
    
    These constants can be used after instantiation in user code if prefixed with instantiated classname
    
        tests.__BME280_ID       # ==  0x77 or 119. this is a fixed address
        tests.__VEML6030_0_ID   # ==  0x10 or 16.  this is the value when the ASW is OFF  
        tests.__VEML6030_1_ID   # ==  0x48 or 72.  this is the value is the ASW is ON  

        tests = PiicoDev_test()
        if tests.is_ID_connected(tests.__BME280_ID):
            print('have BME280')
    
    NOTE: =============================================================================
    NOTE:
    NOTE: The "Constants" and the __TWO__ dictionary lists MUST be checked / updated
    NOTE:    when new PiicoDev devices are created by Core Electronics
    NOTE:     sorry team ;-)
    NOTE:
    NOTE: =============================================================================
    """
    
    #
    # declare "CONSTANTS"
    # these are used to uniquely identify the various (conflicting) PiicoDev addresses
    #  note the 'conflict' markers   ----vv   and    ----^^

    __LED_ID = 0x8				# 8.      RGB LEDS
                                # ----vv
    __VEML6030_0_ID = 0x10		# 16. xx  Light sensor (ASW off)
    __VEML6040_ID = 0x10		# 16. xx  Colour sensor
                                # ----^^
    __LIS3DH_1_ID = 0x18		# 24.     Accelerometer - ASW ON
    __LIS3DH_0_ID = 0x19		# 25.     Accelerometer - ASW OFF
    __TRANSCEIVER_ID = 0x1a		# 26.     Transceiver
    __QMC6310_ID = 0x1c			# 28.     Magnetometer
    __TOUCH_ID = 0x28			# 40.     Capacitive sensor
    __VL53L1X_ID = 0x29			# 41.     Laser distance sensor
    __RFID_ID = 0x2c			# 44.     RFID module
                                # ----vv
    __ULTRASONIC_ID = 0x35		# 53. xx  Ultrasonic rangefinder
    __POTENTIOMETER_ID = 0x35	# 53. xx  Potentiometer
                                # ----^^
    __SSD1306_ID = 0x3c			# 60.     OLED display
    __BUTTON_ID = 0x42			# 66.     Pushbutton
    __SERVO_ID = 0x44			# 68.     Servo controller
                                # ----vv
    __TMP117_ID = 0x48			# 72. xx  Temperature sensor
    __VEML6030_1_ID = 0x48		# 72. xx  Light sensor (ASW on)
                                # ----^^
                                # ----vv
    __RV3028_ID = 0x52			# 82. xx  RTC
    __ENS160_1_ID = 0x52		# 82. xx  Air quality sensor (ASW on)
                                # ----^^
    __ENS160_0_ID = 0x53		# 83.     Air quality sensor (ASW off)
    __BUZZER_ID = 0x5c			# 92.     Buzzer
    __MS5637_ID = 0x76			# 118.    Pressuure sensor
    __BME280_ID = 0x77			# 119.    Atmospheric sensor

    ################
    ## the MAIN list
    ################
    # the dictionary of the fixed, and where possible the default (ASW off) ID's
    #  also has some non-conflicting (ASW on) ID's
    PiicoDev_list: dict = {
        __LED_ID: {			# 8.   0x8
            'what': 'RGB LED Module',
            'long_name': 'PiicoDev 3x RGB LED Module',
            'short_name': 'LED'},
        __VEML6040_ID: {		# 16.  0x10
            'what': 'Colour Sensor',
            'long_name': 'PiicoDev VEML6040 Colour Sensor',
            'short_name': 'VEML6040'},
        __LIS3DH_1_ID: {		# 24.  0x18
            'what': 'Accelerometer (ASW on)',
            'long_name': 'PiicoDev 3-Axis Accelerometer LIS3DH (ASW on)',
            'short_name': 'LIS3DH (ASW on)'},
        __LIS3DH_0_ID: {		# 25.  0x19
            'what': 'Accelerometer (ASW off)',
            'long_name': 'PiicoDev 3-Axis Accelerometer LIS3DH (ASW off)',
            'short_name': 'LIS3DH (ASW off)'},
        __TRANSCEIVER_ID: {		# 26.  0x1A
            'what': 'Transceiver',
            'long_name': 'PiicoDev Transceiver 915MHz',
            'short_name': 'TRANSCEIVER'},
        __QMC6310_ID: {		# 28.  0x1c
            'what': 'Magnetometer',
            'long_name': 'PiicoDev Magnetometer QMC6310',
            'short_name': 'QMC6310'},
        __TOUCH_ID: {		# 40.  0x28
            'what': 'Capacitive Touch Sensor',
            'long_name': 'PiicoDev Capacitive Touch Sensor',
            'short_name': 'TOUCH'},
        __VL53L1X_ID: {		# 41.  0x29
            'what': 'Laser Distance Sensor',
            'long_name': 'PiicoDev Laser Distance Sensor VL53L1X',
            'short_name': 'VL53L1X'},
        __RFID_ID: {		# 45.  0x2c
            'what': 'RFID Module',
            'long_name': 'PiicoDev RFID Module (NFC 13.56MHz)',
            'short_name': 'RFID'},
        __ULTRASONIC_ID: {	# 53.  0x35
           'what': 'Ultrasonic Rangefinder',
            'long_name': 'PiicoDev Ultrasonic Rangefinder Module',
            'short_name': 'ULTRASONIC'},
        __SSD1306_ID: {		# 60.  0x3c
            'what': 'OLED Module',
            'long_name': 'PiicoDev OLED Module SSD1306',
            'short_name': 'SSD1306',
            'initme': 'create_PiicoDev_SSD1306()'},
        __BUTTON_ID: {		# 66.  0x42
            'what': 'Button',
            'long_name': 'PiicoDev Button',
            'short_name': 'BUTTON'},
        __SERVO_ID: {		# 68.  0x44
            'what': 'Servo Driver',
            'long_name': 'PiicoDev Servo Driver (4 Channel)',
            'short_name': 'SERVO'},
        __TMP117_ID: {		# 72.  0x48
            'what': 'Precision Temperature Sensor',
            'long_name': 'PiicoDev TMP117 Precision Temperature Sensor',
            'short_name': 'TMP117'},
        __RV3028_ID: {		# 82.  0x52
            'what': 'Real Time Clock',
            'long_name': 'PiicoDev Real Time Clock (RTC) RV3028',
            'short_name': 'RV3028'},
        __ENS160_0_ID: {		# 83.  0x53
            'what': 'Air Quality Sensor (ASW off)',
            'long_name': 'PiicoDev Air Quality Sensor ENS160 (ASW off)',
            'short_name': 'ENS160 (ASW off)'},
        __BUZZER_ID: {		# 92.  0x5c
            'what': 'Buzzer Module',
            'long_name': 'PiicoDev Buzzer Module',
            'short_name': 'BUZZER'},
        __MS5637_ID: {		# 118.  0x76
            'what': 'Pressure Sensor',
            'long_name': 'PiicoDev Pressure Sensor MS5637',
            'short_name': 'MS5637'},
        __BME280_ID: {		# 119.  0x77
            'what': 'Atmospheric Sensor',
            'long_name': 'PiicoDev BME280 Atmospheric Sensor',
            'short_name': 'BME280'},
    }

    #####################
    ## the conflicts list
    #####################
    # the dictionary of the conflicting fixed, and conflicting (ASW on) ID's
    #  also has some conflicting (ASW off) ID's
    PiicoDev_conf_list: dict = {
        __VEML6030_0_ID: {		# 16.  0x10
            'what': 'Ambient Light Sensor (ASW off)',
            'long_name': 'PiicoDev VEML6030 Ambient Light Sensor (ASW off)',
            'short_name': 'VEML6030 (ASW off)'},
        __POTENTIOMETER_ID: {	# 53.  0x35
           'what': 'Potentiometer',
            'long_name': 'PiicoDev Potentiometer (Rotary)',
            'short_name': 'Potentiometer'},
        __VEML6030_1_ID: {	# 72.  0x48
            'what': 'Ambient Light Sensor (ASW on)',
            'long_name': 'PiicoDev VEML6030 Ambient Light Sensor (ASW on)',
            'short_name': 'VEML6030 (ASW on)'},
        __ENS160_1_ID: {		# 82.  0x52
            'what': 'Air Quality Sensor (ASW on)',
            'long_name': 'PiicoDev Air Quality Sensor ENS160 (ASW on)',
            'short_name': 'ENS160 (ASW on)'},
    }

    #
    # PiicoDev defaults pre-defined
    # can be overloaded with other values if needed to establish a second/alternate i2c bus
    #
    def __init__(self, id=0, scl=Pin(9), sda=Pin(8), freq=400_000):
        self.i2c = I2C(id=id, scl=scl, sda=sda, freq=freq)
        self.connected = self.i2c.scan()
        
    # clear() - clears the list of connected i2c devices
    def clear(self):
        self.connected = []
        
    # rescan() - clears and rescans the default i2c bus and repopulates the list
    def rescan(self):
        self.connected = []
        self.connected = self.i2c.scan()
    
    # show_int() - prints the list of connected ID's in DECIMAL detected by the original/most recent scan
    def show_int(self):
        print(self.connected)
    
    # show_hex() - prints the list of connected ID's in HEXADECIMAL detected by the original/most recent scan
    def show_hex(self):
        print( [hex(i) for i in self.connected] )

    # is_ID_connected(id) - returns 1 if the ID is in the list, otherwise 0
    def is_ID_connected(self, id):
        if _Debug == 1:
            print('is_ID_connected(',id,')')
        if self.connected.count(id) == 1:
            return(1)
        else:
            return(0)
    
    # how_many_connected() - returns count of detected ID's
    def how_many_connected(self):
        if _Debug == 1:
            print('how_many__connected()')
        return(len(self.connected))

    # details() - prints various levels of information of the connected ID's
    def details(self, mode='what', extlist=None):
        if _Debug == 1:
            print('details(',mode,')')
        if len(self.connected) == 0:
            print('Nothing connected')
        else:
            for i in self.connected:
                hit = 0
                if i in self.PiicoDev_list:
                    self.print_main(i, mode)
                    hit = 1
                if i in self.PiicoDev_conf_list:
                    print('   vvv Possible conflict vvv')
                    self.print_conf(i, mode)
                    hit = 1
                if extlist != None:
                    if i in extlist:
                        print('   vvv EXTERNAL LIST --- Possible conflict vvv')
                        if mode == 'long':
                            s = extlist[i]['long_name']
                        elif mode == 'short':
                            s = extlist[i]['short_name']
                        else:   # assume 'what'
                            s = extlist[i]['what']
                        print(i, hex(i), s)
                        hit = 1
                if hit == 0:
                    print('Unknown device at ID ', i)

    # what_is(id) - prints various levels of information from the dictionaries of the given ID
    def what_is(self, id, mode='what', extlist=None):
        hit = 0
        if id in self.PiicoDev_list:
            self.print_main(id, mode)
            hit = 1  # found it here
        if id in self.PiicoDev_conf_list:
            if hit == 1:  # have we already found it?
                print('   vvv Possible conflict vvv')
            self.print_conf(id, mode)
            hit = 1 # set this so so we can test for external conflicts also
        if extlist != None:
            if id in extlist:
                if hit == 1:  # have we already found it at least once?
                    print('   vvv Possible EXTERNAL conflict vvv')
                self.print_ext(id, mode, extlist)
                hit = 1 # set this so we don't trigger the next line
        if hit == 0:
            print('Unknown ID ', id)

    # show_all() - prints various levels of information from the main/conflict internal dictonaries
    def show_all(self, mode='what', conf=None, extlist=None ):
        for i in sorted(self.PiicoDev_list):
            self.print_main(i, mode)
        if conf != None:
            print('-- conflicting --')
            for i in sorted(self.PiicoDev_conf_list):
                self.print_conf(i, mode)
        if extlist != None:
            print('-- external list --')
            for i in sorted(extlist):
                self.print_ext(i,mode,extlist)
                
    # Print common functions
    # print information from  the main dictionary
    def print_main(self, id, mode):
        if mode == 'long':
            s = self.PiicoDev_list[id]['long_name']
        elif mode == 'short':
            s = self.PiicoDev_list[id]['short_name']
        else:   # assume 'what'
            s = self.PiicoDev_list[id]['what']
        print(id, hex(id), s)

    # print information from  the conflicts dictionary
    def print_conf(self, id, mode):
        if mode == 'long':
            s = self.PiicoDev_conf_list[id]['long_name']
        elif mode == 'short':
            s = self.PiicoDev_conf_list[id]['short_name']
        else:   # assume 'what'
            s = self.PiicoDev_conf_list[id]['what']
        print(id, hex(id), s)

    # print information from the external user dictionary
    def print_ext(self, i, mode, extlist):
        if mode == 'long':
            s = extlist[i]['long_name']
        elif mode == 'short':
            s = extlist[i]['short_name']
        else:   # assume 'what'
            s = extlist[i]['what']
        print(i, hex(i), s)

#
# end of  class
#
###########################################

if _Debug:
    tests = Piico_info()

    # for an alternate i2c bus on GPIO6 and GPOI7
    test_altbus = Piico_info(id=1, scl=Pin(7), sda=Pin(6))

    print('tests.connected')
    print(tests.connected)
    print('clear()')
    tests.clear()
    print(tests.connected)
    print('rescan()')
    tests.rescan()
    print(tests.connected)
    print('show()')
    tests.show_int()
    tests.show_hex()
    print('how many')
    aa = tests.how_many_connected()
    print(aa)
    print('details()')
    tests.details()
    tests.details('short')
    tests.details('long')
    aa = tests.is_ID_connected(119)
    print(aa)

    aa = tests.is_ID_connected(0x77)
    print(aa)

    if tests.is_ID_connected(tests.__BME280_ID):
        print('have BME280')

    if tests.is_ID_connected(tests.__POTENTIOMETER_ID):
        print('have Ultrasonic rangfinder - cant distinguish conflicting IDs')
    else:
        print('oops')
        
    tests.what_is(0xff)	# no such ID, will complain
    
    tests.what_is(53, 'long')

    tests.show_all()

    tests.show_all('long','show')

    print('***************************************************')
