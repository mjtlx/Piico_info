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

    # the default for standard PiicoDev setup
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

#### details()

The details() function accesses a pre-defined dictionary of devices made by core Electronics
and displays information about _ALL_ connected devices

    details()           - prints 'human name' of the connected ID's e.g. 'OLED Module' (default is 'what')
    details('what')     - prints 'human name' of the connected ID's e.g. 'OLED Module'    
    details('short')    - prints 'short_name' of the connected ID's e.g. 'SSD1306'
    details('long')     - prints 'long_name' of the connected ID's e.g. 'PiicoDev OLED Module SSD1306'

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

#### what_is()

The what_is() function accesses a pre-defined dictionary of devices made by core Electronics
and displays information about the device with the specified id in hex or decimal or by a prefefined constant (see below)

    what_is(id)             - prints 'human name' of the given ID e.g. 'RGB LED Module' (default is 'what')
    what_is(id, 'what')     - prints 'human name' of the given ID e.g. 'RGB LED Module'
    what_is(id, 'short')    - prints 'short_name' of the given ID e.g. 'LED'
    what_is(id, 'long')     - prints 'long_name' of the given ID e.g. 'PiicoDev 3x RGB LED Module'

### show_all()

The show_all() function accesses a pre-defined dictionary of devices made by core Electronics
and displays all the selected information 'type'

    show_all()          - prints all 'human names' from the main internal dictonary (default is 'what')
    show_all('what')    - prints all 'human names' from the main internal dictonary
    show_all('short')   - prints all 'short names' from the main internal dictonary
    show_all('long')    - prints all 'long names' from the main internal dictonary
        
##### Show option
  
With extra option 'show' also displays similar entries from the conflicts dictionary (see below)
  
    show_all('what', 'show')    - prints all 'human names' from the conflict internal dictonary
    show_all('short', show')    - prints all 'shout names' from the conflict internal dictonary
    show_all('long', 'show')    - prints all 'long names' from the conflict internal dictonary
            
## Address conflicts

Where appropriate this module will provide information about potential conflicts, since some PiicoDev devices
do have addresses that could collide. This can be dealt with by setting the module address switch (ASW)
to a non default setting (if available), OR by programatically changing the device address if possible.
    
This module only 'knows' about PiicoDev devices, however an external dictionary can be provided by the user.
    
** The module CANNOT detect an actual address conflict on a given i2c bus. This is a characteristic of the bus itself.
    
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

