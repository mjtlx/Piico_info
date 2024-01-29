# Piico_info (a.k.a. PiicoDev devices presence tests)

This library provides support for the Core electronics PiicoDev system, generating information about connected devices.  
    Murray T 20240128   (v 1.0)
    @Murray125532

## Simple tests that can be done without this module

    i2c = I2C(id=0)         # PiicoDev chain on i2c channel 0
    connected = i2c.scan()  # whats connected
    print(connected)        # prints decimal list
    for i in connected:     # prints hexadecimal list
        print(i, hex(i))    #  /

# Using this module

## Instantiation

	# import the library code
	from Piico_info import Piico_info
	 
    # then instantiate it (this is the default for standard PiicoDev setup)
    tests = Piico_info()
    
OR

    # for an alternate i2c bus on GPIO6 and GPOI7
    test_altbus = Piico_info(id=1, scl=Pin(7), sda=Pin(6))
    
Immediately after this you can display what has been detected on the default i2c bus by either
    
    print(tests.connected)
    
OR

    tests.show_int()

these print a list of detected i2c ID's in decimal
    [16, 60, 82, 83, 119]
        
## Available functions

### Basic functions

    clear()                 - clears the list of connected i2c devices
    rescan()                - clears and rescans the default i2c bus and repopulates the list
    show_int()              - prints the list of connected ID's in DECIMAL detected by the original/most recent scan
    show_hex()              - prints the list of connected ID's in HEXADECIMAL detected by the original/most recent scan
    is_ID_connected(id)     - returns 1 if the ID is in the list, otherwise 0
    how_many_connected()    - returns count of detected ID's

### Functions returning more info

### details()

The details() function accesses a pre-defined dictionary of devices made by core Electronics
and displays information about _ALL_ connected devices

    details()           - prints 'human name' of the connected ID's e.g. 'OLED Module' (default is 'what')
    details('what')     - prints 'human name' of the connected ID's e.g. 'OLED Module'    
    details('short')    - prints 'short_name' of the connected ID's e.g. 'SSD1306'
    details('long')     - prints 'long_name' of the connected ID's e.g. 'PiicoDev OLED Module SSD1306'

#### External User dictionary

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

Calling the details() function as below _AFTER_ the user dictionary is defined, will
display this if the LTR390 is in the connected devices list, as well as info about other connected PiicoDev devices.
        
    details('what', extern_list ) - prints 'human name' of the connected ID's e.g. 'Ambient Light-UV Sensor'       
    details('short', extern_list) - prints 'short_name' of the connected ID's e.g. 'LTR390'
    details('long', extern_list)  - prints 'long_name' of the connected ID's e.g. 'Adafruit LTR390 Ambient Light-UV Sensor'

### what_is()

The what_is() function accesses a pre-defined dictionary of devices made by Core Electronics
and displays information about the device with the specified id in hex or decimal or by a prefefined constant (see below)

    what_is(id)             - prints 'human name' of the given ID e.g. 'RGB LED Module' (default is 'what')
    what_is(id, 'what')     - prints 'human name' of the given ID e.g. 'RGB LED Module'
    what_is(id, 'short')    - prints 'short_name' of the given ID e.g. 'LED'
    what_is(id, 'long')     - prints 'long_name' of the given ID e.g. 'PiicoDev 3x RGB LED Module'

#### External User dictionary

The what_is() function can also access a user defined dictionary of devices from other manufacturers.

    what_is(id, extern_list)             - prints 'human name' of the given ID e.g. 'RGB LED Module' (default is 'what')
    what_is(id, 'what', extern_list)     - prints 'human name' of the given ID e.g. 'RGB LED Module'
    what_is(id, 'short', extern_list)    - prints 'short_name' of the given ID e.g. 'LED'
    what_is(id, 'long', extern_list)     - prints 'long_name' of the given ID e.g. 'PiicoDev 3x RGB LED Module'

**NOTE:** in both cases, what_is() will highlight potential address conflicts 

### show_all()

The show_all() function accesses a pre-defined dictionary of devices made by core Electronics
and displays all the selected information 'type'

    show_all()          - prints all 'human names' from the main internal dictonary (default is 'what')
    show_all('what')    - prints all 'human names' from the main internal dictonary
    show_all('short')   - prints all 'short names' from the main internal dictonary
    show_all('long')    - prints all 'long names' from the main internal dictonary
        
##### Show option
  
With extra option 'show' also displays similar entries from the conflicts dictionary (see below)
  
    show_all('what', 'show')    - prints all 'human names' from both internal dictonaries
    show_all('short', 'show')    - prints all 'short names' from both internal dictonaries
    show_all('long', 'show')    - prints all 'long names' from both internal dictonaries

#### External User dictionary

The show_all() function can also access a user defined dictionary of devices from other manufacturers.

    show_all('what', 'show', extern_list)    - prints all 'human names' from both internal dictonaries
                                		AND the external user defined dictionary
    show_all('short', extern_list)    - prints all 'short names' from the main internal dictonary
                                		AND the external user defined dictionary
    show_all('long', 'show', extern_list)    - prints all 'long names' from both internal dictonaries
                                		AND the external user defined dictionary
            
## Address conflicts

Where appropriate this module will provide information about potential conflicts, since some PiicoDev devices
do have addresses that could collide. This can be dealt with by setting the module address switch (ASW)
to a non default setting (if available), OR by programatically changing the device address if possible.
    
This module only 'knows' about PiicoDev devices, however an external dictionary can be provided by the user.
    
**NOTE:** The module CANNOT detect an actual address conflict on a given i2c bus. This is a characteristic of the bus itself.
    
## 'Constant' values

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
    
## Internal updates

The "Constants" and the __TWO__ dictionary lists (main and conflicts) MUST be checked / updated
when new PiicoDev devices are created by Core Electronics. 

# Example use

The PiicoDev devices connected to the test system were:

- Oled display                          Address 0x3C (60.)
- BME280 sensor Atmospheric sensor      Address 0x77 (119.)
- ENS160 Air quality sensor             Address 0x52 (82.) - ASW on
- VEML6030 ambient light sensor         Address 0x10 (16.)
- (AdaFruit) LTR390 Ambient/UV sensor   Address 0x53 (83.)

NOTE: the default address for the ENS160 is 0x53, but to avoid conflict with the LTR390, the 
Address Switch has been set ON, which sets the address to 0x52.

## Code

This code should output the result in the next section.

```
import PiicoDev_Unified
from Piico_info import Piico_info

print('********** Example start ************************')
print('\n>> instantiate')
tests = Piico_info()

# for an alternate i2c bus on GPIO6 and GPOI7
#    test_altbus = Piico_info(id=1, scl=Pin(7), sda=Pin(6))

print('\n>> tests.connected')
print(tests.connected)

print('\n>> clear()')
tests.clear()

print('... and show list')
print(tests.connected)

print('\n>> rescan()')
tests.rescan()
print('... and show list')
print(tests.connected)

print('\n>> show_int()')
tests.show_int()
print('\n>> show_hex()')
tests.show_hex()

print('\n>> how_many_connected()')
print( tests.how_many_connected() )

print('\n>> is_ID_connected(119) -- decimal id')
print( tests.is_ID_connected(119) )

print('\n>> is_ID_connected(0x77) -- hex id')
print( tests.is_ID_connected(0x77) )

print('\n>> is_ID_connected(tests.__BME280_ID) -- \'Constant id\', device has unique address ')
if tests.is_ID_connected(tests.__BME280_ID):
    print('have BME280')
print('\n>> is_ID_connected(tests.__POTENTIOMETER_ID) -- \'Constant id\', device is a possible conflicting address ')
if tests.is_ID_connected(tests.__POTENTIOMETER_ID):
    print('something is connected, probably Ultrasonic rangefinder since cant distinguish conflicting IDs')
else:
    print('oops. no actual device connected.')
      
print('\n>> details()')
tests.details()
print('\n>> details(\'short\')')
tests.details('short')
print('\n>> details(\'long\')')
tests.details('long')

print('\n>> Define a additional dictionary with your own device(s)')
print('extern_list: dict = {')
print('    0x53: {		# 16.  0x10')
print('        \'what\': \'Ambient Light-UV Sensor\',')
print('        \'long_name\': \'Adafruit LTR390 Ambient Light-UV Sensor\',')
print('        \'short_name\': \'LTR390\'},')
print('    }')

extern_list: dict = {
    0x53: {		# 83.  0x53
        'what': 'Ambient Light-UV Sensor',
        'long_name': 'Adafruit LTR390 Ambient Light-UV Sensor',
        'short_name': 'LTR390'},
    }

print('\n>> Now the details() function can also use the new dictionary')
print('>> details(\'long\', extern_list) -- add the external list to the function call')
tests.details('long', extern_list)

print('\n>> what_is(0xff) -- NB invalid id value')
tests.what_is(0xff)	# no such ID, will complain
    
print('\n>> what_is(53, \'long\')')
tests.what_is(53, 'long')

print('\n>> The what_is() function can also use the external dictionary')
print('>> what_is(83, \'long\', extern_list) -- add the external list to the function call')
tests.what_is(83, 'long', extern_list)

print('\n>> show_all()')
tests.show_all()

print('\n>> show_all(\'long\',\'show\')')
tests.show_all('long','show')

print('\n>> The show_all() function can also use the external dictionary')
print('>> show_all(\'long\',\'show\', extern_list) -- add the external list to the function call')
tests.show_all('long','show', extern_list)

print('\n********** Example complete ************************')
```

## Output of Example

```
********** Example start ************************

>> instantiate

>> tests.connected
[16, 60, 82, 83, 119]

>> clear()
... and show list
[]

>> rescan()
... and show list
[16, 60, 82, 83, 119]

>> show_int()
[16, 60, 82, 83, 119]

>> show_hex()
['0x10', '0x3c', '0x52', '0x53', '0x77']

>> how_many_connected()
5

>> is_ID_connected(119) -- decimal id
1

>> is_ID_connected(0x77) -- hex id
1

>> is_ID_connected(tests.__BME280_ID) -- 'Constant id', device has unique address 
have BME280

>> is_ID_connected(tests.__POTENTIOMETER_ID) -- 'Constant id', device is a possible conflicting address 
oops. no actual device connected.

>> details()
16 0x10 Colour Sensor
   vvv Possible conflict vvv
16 0x10 Ambient Light Sensor (ASW off)
60 0x3c OLED Module
82 0x52 Real Time Clock
   vvv Possible conflict vvv
82 0x52 Air Quality Sensor (ASW on)
83 0x53 Air Quality Sensor (ASW off)
119 0x77 Atmospheric Sensor

>> details('short')
16 0x10 VEML6040
   vvv Possible conflict vvv
16 0x10 VEML6030 (ASW off)
60 0x3c SSD1306
82 0x52 RV3028
   vvv Possible conflict vvv
82 0x52 ENS160 (ASW on)
83 0x53 ENS160 (ASW off)
119 0x77 BME280

>> details('long')
16 0x10 PiicoDev VEML6040 Colour Sensor
   vvv Possible conflict vvv
16 0x10 PiicoDev VEML6030 Ambient Light Sensor (ASW off)
60 0x3c PiicoDev OLED Module SSD1306
82 0x52 PiicoDev Real Time Clock (RTC) RV3028
   vvv Possible conflict vvv
82 0x52 PiicoDev Air Quality Sensor ENS160 (ASW on)
83 0x53 PiicoDev Air Quality Sensor ENS160 (ASW off)
119 0x77 PiicoDev BME280 Atmospheric Sensor

>> Define a additional dictionary with your own device(s)
extern_list: dict = {
    0x53: {		# 16.  0x10
        'what': 'Ambient Light-UV Sensor',
        'long_name': 'Adafruit LTR390 Ambient Light-UV Sensor',
        'short_name': 'LTR390'},
    }

>> Now the details() function can also use the new dictionary
>> details('long', extern_list) -- add the external list to the function call
16 0x10 PiicoDev VEML6040 Colour Sensor
   vvv Possible conflict vvv
16 0x10 PiicoDev VEML6030 Ambient Light Sensor (ASW off)
60 0x3c PiicoDev OLED Module SSD1306
82 0x52 PiicoDev Real Time Clock (RTC) RV3028
   vvv Possible conflict vvv
82 0x52 PiicoDev Air Quality Sensor ENS160 (ASW on)
83 0x53 PiicoDev Air Quality Sensor ENS160 (ASW off)
   vvv EXTERNAL LIST --- Possible conflict vvv
83 0x53 Adafruit LTR390 Ambient Light-UV Sensor
119 0x77 PiicoDev BME280 Atmospheric Sensor

>> what_is(0xff) -- NB invalid id value
Unknown ID  255

>> what_is(53, 'long')
53 0x35 PiicoDev Ultrasonic Rangefinder Module
   vvv Possible conflict vvv
53 0x35 PiicoDev Potentiometer (Rotary)

>> The what_is() function can also use the external dictionary
>> what_is(83, 'long', extern_list) -- add the external list to the function call
83 0x53 PiicoDev Air Quality Sensor ENS160 (ASW off)
   vvv Possible EXTERNAL conflict vvv
83 0x53 Adafruit LTR390 Ambient Light-UV Sensor

>> show_all()
8 0x8 RGB LED Module
16 0x10 Colour Sensor
24 0x18 Accelerometer (ASW on)
25 0x19 Accelerometer (ASW off)
26 0x1a Transceiver
28 0x1c Magnetometer
40 0x28 Capacitive Touch Sensor
41 0x29 Laser Distance Sensor
44 0x2c RFID Module
53 0x35 Ultrasonic Rangefinder
60 0x3c OLED Module
66 0x42 Button
68 0x44 Servo Driver
72 0x48 Precision Temperature Sensor
82 0x52 Real Time Clock
83 0x53 Air Quality Sensor (ASW off)
92 0x5c Buzzer Module
118 0x76 Pressure Sensor
119 0x77 Atmospheric Sensor

>> show_all('long','show')
8 0x8 PiicoDev 3x RGB LED Module
16 0x10 PiicoDev VEML6040 Colour Sensor
24 0x18 PiicoDev 3-Axis Accelerometer LIS3DH (ASW on)
25 0x19 PiicoDev 3-Axis Accelerometer LIS3DH (ASW off)
26 0x1a PiicoDev Transceiver 915MHz
28 0x1c PiicoDev Magnetometer QMC6310
40 0x28 PiicoDev Capacitive Touch Sensor
41 0x29 PiicoDev Laser Distance Sensor VL53L1X
44 0x2c PiicoDev RFID Module (NFC 13.56MHz)
53 0x35 PiicoDev Ultrasonic Rangefinder Module
60 0x3c PiicoDev OLED Module SSD1306
66 0x42 PiicoDev Button
68 0x44 PiicoDev Servo Driver (4 Channel)
72 0x48 PiicoDev TMP117 Precision Temperature Sensor
82 0x52 PiicoDev Real Time Clock (RTC) RV3028
83 0x53 PiicoDev Air Quality Sensor ENS160 (ASW off)
92 0x5c PiicoDev Buzzer Module
118 0x76 PiicoDev Pressure Sensor MS5637
119 0x77 PiicoDev BME280 Atmospheric Sensor
-- conflicting --
16 0x10 PiicoDev VEML6030 Ambient Light Sensor (ASW off)
53 0x35 PiicoDev Potentiometer (Rotary)
72 0x48 PiicoDev VEML6030 Ambient Light Sensor (ASW on)
82 0x52 PiicoDev Air Quality Sensor ENS160 (ASW on)

>> The show_all() function can also use the external dictionary
>> show_all('long','show', extern_list) -- add the external list to the function call
8 0x8 PiicoDev 3x RGB LED Module
16 0x10 PiicoDev VEML6040 Colour Sensor
24 0x18 PiicoDev 3-Axis Accelerometer LIS3DH (ASW on)
25 0x19 PiicoDev 3-Axis Accelerometer LIS3DH (ASW off)
26 0x1a PiicoDev Transceiver 915MHz
28 0x1c PiicoDev Magnetometer QMC6310
40 0x28 PiicoDev Capacitive Touch Sensor
41 0x29 PiicoDev Laser Distance Sensor VL53L1X
44 0x2c PiicoDev RFID Module (NFC 13.56MHz)
53 0x35 PiicoDev Ultrasonic Rangefinder Module
60 0x3c PiicoDev OLED Module SSD1306
66 0x42 PiicoDev Button
68 0x44 PiicoDev Servo Driver (4 Channel)
72 0x48 PiicoDev TMP117 Precision Temperature Sensor
82 0x52 PiicoDev Real Time Clock (RTC) RV3028
83 0x53 PiicoDev Air Quality Sensor ENS160 (ASW off)
92 0x5c PiicoDev Buzzer Module
118 0x76 PiicoDev Pressure Sensor MS5637
119 0x77 PiicoDev BME280 Atmospheric Sensor
-- conflicting --
16 0x10 PiicoDev VEML6030 Ambient Light Sensor (ASW off)
53 0x35 PiicoDev Potentiometer (Rotary)
72 0x48 PiicoDev VEML6030 Ambient Light Sensor (ASW on)
82 0x52 PiicoDev Air Quality Sensor ENS160 (ASW on)
-- external list --
83 0x53 Adafruit LTR390 Ambient Light-UV Sensor

********** Example complete ************************
```
