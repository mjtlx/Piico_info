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
    0x53: {		# 16.  0x10
        'what': 'Ambient Light-UV Sensor',
        'long_name': 'Adafruit LTR390 Ambient Light-UV Sensor',
        'short_name': 'LTR390'},
    }

print('\n>> Now the details() function can also use the new dictionary')
print('>> details(\'long\', extern_list) -- add the external list to the function call')
tests.details('long', extern_list)

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
      
print('\n>> what_is(0xff) -- NB invalid id value')
tests.what_is(0xff)	# no such ID, will complain
    
print('\n>> what_is(53, \'long\')')
tests.what_is(53, 'long')

print('\n>> show_all()')
tests.show_all()

print('\n>> show_all(\'long\',\'show\')')
tests.show_all('long','show')

print('\n********** Example complete ************************')

