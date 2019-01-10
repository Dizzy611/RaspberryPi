#!/usr/bin/python
"""Raspberry Pi OTP Dump Parser

 Copyright 2019 Jasmine Iwanek & Dylan Morrison

 Permission is hereby granted, free of charge, to any person obtaining a copy of this
 software and associated documentation files (the "Software"), to deal in the Software
 without restriction, including without limitation the rights to use, copy, modify, merge,
 publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
 to whom the Software is furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all copies or
 substantial portions of the Software.

 THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
 PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
 FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
 OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 DEALINGS IN THE SOFTWARE.

 Usage
 call either ./OTPParser.py <filename> or vgcencmd otp_dump | OTPParser
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
from string import hexdigits
from os import path

if (sys.version_info < (2, 6) or (sys.version_info >= (3, 0) and sys.version_info < (3, 3))):
    sys.exit('OTPParser requires Python 2.6 or 3.3 and newer.')

try:
    from future import standard_library
    standard_library.install_aliases()
except ImportError:
    sys.exit('OTPParser requires future!')

try:
    from builtins import dict, hex, int, open, range, str
except ImportError:
    sys.exit("OTPParser requires future! (Cant import 'builtins'")


class TypoError(Exception):
    """TypoError exception."""
    pass


MEMORY_SIZES = {
    '256':       '000',    # 0
    '512':       '001',    # 1
    '1024':      '010',    # 2
    'unknown_3': '011',    # 3
    'unknown_4': '100',    # 4
    'unknown_5': '101',    # 5
    'unknown_6': '110',    # 6
    'unknown_7': '111',    # 7
    '256/512':   'EITHER',
    'unknown':   ''
}
MEMORY_SIZES_AS_STRING = dict((v, k) for k, v in list(MEMORY_SIZES.items()))

MANUFACTURERS = {
    'Sony UK':    '0000',  # 0
    'Egoman':     '0001',  # 1
    'Embest':     '0010',  # 2
    'Sony Japan': '0011',  # 3
    'Embest #2':  '0100',  # 4
    'Stadium':    '0101',  # 5
    'unknown_6':  '0110',  # 6
    'unknown_7':  '0111',  # 7
    'unknown_8':  '1000',  # 8
    'unknown_9':  '1001',  # 9
    'unknown_a':  '1010',  # a
    'unknown_b':  '1011',  # b
    'unknown_c':  '1100',  # c
    'unknown_d':  '1101',  # d
    'unknown_e':  '1110',  # e
    'unknown_f':  '1111',  # f
    'Qisda':      'QISD',  # Correct value unknown
    'unknown':    ''
}
MANUFACTURERS_AS_STRING = dict((v, k) for k, v in list(MANUFACTURERS.items()))

PROCESSORS = {
    'BCM2835':   '0000',  # 0
    'BCM2836':   '0001',  # 1
    'BCM2837':   '0010',  # 2
    'unknown_3': '0011',  # 3
    'unknown_4': '0100',  # 4
    'unknown_5': '0101',  # 5
    'unknown_6': '0110',  # 6
    'unknown_7': '0111',  # 7
    'unknown_8': '1000',  # 8
    'unknown_9': '1001',  # 9
    'unknown_a': '1010',  # a
    'unknown_b': '1011',  # b
    'unknown_c': '1100',  # c
    'unknown_d': '1101',  # d
    'unknown_e': '1110',  # e
    'unknown_f': '1111',  # f
    'unknown':   ''

}
PROCESSORS_AS_STRING = dict((v, k) for k, v in list(PROCESSORS.items()))

BOARD_TYPES = {
    'A':         '00000000',  # 0
    'B':         '00000001',  # 1
    'A+':        '00000010',  # 2
    'B+':        '00000011',  # 3
    '2B':        '00000100',  # 4
    'Alpha':     '00000101',  # 5
    'CM1':       '00000110',  # 6
    'Unknown_7': '00000111',  # 7 (Not in known use)
    '3B':        '00001000',  # 8
    'Zero':      '00001001',  # 9
    'CM3':       '00001010',  # a
    'Unknown_b': '00001011',  # b (Not in known use)
    'Zero W':    '00001100',  # c
    '3B+':       '00001101',  # d
    '3A+':       '00001110',  # e
    'unknown_f': '00001111',  # f (Not in known use)
    'unknown':   ''
}
BOARD_TYPES_AS_STRING = dict((v, k) for k, v in list(BOARD_TYPES.items()))

BOARD_REVISIONS = {
    '1.0':       '0000',
    '1.1':       '0001',
    '1.2':       '0010',
    '1.3':       '0011',
    'unknown_4': '0100',
    'unknown_5': '0101',
    'unknown_6': '0110',
    'unknown_7': '0111',
    'unknown_8': '1000',
    'unknown_9': '1001',
    'unknown_a': '1010',
    'unknown_b': '1011',
    'unknown_c': '1100',
    'unknown_d': '1101',
    'unknown_e': '1110',
    'unknown_f': '1111',
    '2.0':       ' 2.0',  # Correct Value unknown.
    'unknown':   ''
}
BOARD_REVISIONS_AS_STRING = dict((v, k) for k, v in list(BOARD_REVISIONS.items()))

LEGACY_REVISIONS = {
    '00010': {'memory_size': '256', 'manufacturer': 'Egoman',
              'processor': 'BCM2835', 'board_type': 'B', 'board_revision': '1.0'},
    '00011': {'memory_size': '256', 'manufacturer': 'Egoman',
              'processor': 'BCM2835', 'board_type': 'B', 'board_revision': '1.0'},
    '00100': {'memory_size': '256', 'manufacturer': 'Sony UK',
              'processor': 'BCM2835', 'board_type': 'B', 'board_revision': '2.0'},
    '00101': {'memory_size': '256', 'manufacturer': 'Qisda',
              'processor': 'BCM2835', 'board_type': 'B', 'board_revision': '2.0'},
    '00110': {'memory_size': '256', 'manufacturer': 'Egoman',
              'processor': 'BCM2835', 'board_type': 'B', 'board_revision': '2.0'},
    '00111': {'memory_size': '256', 'manufacturer': 'Egoman',
              'processor': 'BCM2835', 'board_type': 'A', 'board_revision': '2.0'},
    '01000': {'memory_size': '256', 'manufacturer': 'Sony UK',
              'processor': 'BCM2835', 'board_type': 'A', 'board_revision': '2.0'},
    '01001': {'memory_size': '256', 'manufacturer': 'Qisda',
              'processor': 'BCM2835', 'board_type': 'A', 'board_revision': '2.0'},
    '01101': {'memory_size': '512', 'manufacturer': 'Egoman',
              'processor': 'BCM2835', 'board_type': 'B', 'board_revision': '2.0'},
    '01110': {'memory_size': '512', 'manufacturer': 'Sony UK',
              'processor': 'BCM2835', 'board_type': 'B', 'board_revision': '2.0'},
    '01111': {'memory_size': '512', 'manufacturer': 'Egoman',
              'processor': 'BCM2835', 'board_type': 'B', 'board_revision': '2.0'},
    '10000': {'memory_size': '512', 'manufacturer': 'Sony UK',
              'processor': 'BCM2835', 'board_type': 'B+', 'board_revision': '1.0'},
    '10001': {'memory_size': '512', 'manufacturer': 'Sony UK',
              'processor': 'BCM2835', 'board_type': 'CM1', 'board_revision': '1.0'},
    '10010': {'memory_size': '512', 'manufacturer': 'Sony UK',
              'processor': 'BCM2835', 'board_type': 'A+', 'board_revision': '1.1'},
    '10011': {'memory_size': '512', 'manufacturer': 'Embest',
              'processor': 'BCM2835', 'board_type': 'B+', 'board_revision': '1.2'},
    '10100': {'memory_size': '512', 'manufacturer': 'Embest',
              'processor': 'BCM2835', 'board_type': 'CM1', 'board_revision': '1.0'},
    '10101': {'memory_size': '256/512', 'manufacturer': 'Embest',
              'processor': 'BCM2835', 'board_type': 'A+', 'board_revision': '1.1'},
    'default': {'memory_size': 'unknown', 'manufacturer': 'unknown',
                'processor': 'unknown', 'board_type': 'unknown', 'board_revision': 'unknown'}
}

REGIONS = {
    'unknown_8':               8,
    'unknown_9':               9,
    'unknown_10':             10,
    'unknown_11':             11,
    'unknown_12':             12,
    'unknown_13':             13,
    'unknown_14':             14,
    'unknown_15':             15,
    'unknown_16':             16,  # Usually 00280000, sometimes 2428000 or 6c28000, as yet unknown
    'bootmode':               17,  # BootMode Register
    'bootmode_copy':          18,  # Backup copy of BootMode Register
    'unknown_19':             19,  # Always ffffffff in tests
    'unknown_20':             20,  # Always ffffffff in tests
    'unknown_21':             21,  # Always ffffffff in tests
    'unknown_22':             22,  # Always ffffffff in tests
    'unknown_23':             23,  # Always ffffffff in tests
    'unknown_24':             24,  # Always ffffffff in tests
    'unknown_25':             25,  # Always ffffffff in tests
    'unknown_26':             26,  # Always ffffffff in tests
    'unknown_27':             27,  # Has varying values, as yet unknown
    'serial_number':          28,  # Serial Number
    'serial_number_inverted': 29,  # Serial Number (Bitflipped)
    'revision_number':        30,  # Revision Number
    'batch_number':           31,  # Batch Number
    'overclock':              32,  # Overclock Register
    'unknown_33':             33,
    'unknown_34':             34,
    'unknown_35':             35,
    'customer_one':           36,  #
    'customer_two':           37,  #
    'customer_three':         38,  #
    'customer_four':          39,  #
    'customer_five':          40,  #
    'customer_six':           41,  #
    'customer_seven':         42,  #
    'customer_eight':         43,  #
    'unknown_44':             44,
    'codec_key_one':          45,  # Codec License Key #1
    'codec_key_two':          46,  # Codec License Key #2
    'unknown_47':             47,
    'unknown_48':             48,
    'unknown_49':             49,
    'unknown_50':             50,
    'unknown_51':             51,
    'unknown_52':             52,
    'unknown_53':             53,
    'unknown_54':             54,
    'unknown_55':             55,
    'unknown_56':             56,
    'unknown_57':             57,
    'unknown_58':             58,
    'unknown_59':             59,
    'unknown_60':             60,
    'unknown_61':             61,
    'unknown_62':             62,
    'unknown_63':             63,
    'mac_address_two':        64,  # MAC Address (Second part)
    'mac_address_one':        65,  # MAC Address (First part)
    'advanced_boot':          66,  # Advanced Boot Register
}

BOARD = {
    'memory':        '000',
    'manufacturer': '0000',
    'processor':    '0000',
    'type':     '00000000',
    'revision':     '0000'
}

DATA = {}


def is_hex(string):
    """Check if the string is hexidecimal.
    Credit to eumiro, stackoverflow:
    https://stackoverflow.com/questions/11592261/check-if-a-string-is-hexadecimal
    """
    hex_digits = set(hexdigits)
    # if string is long, then it is faster to check against a set
    return all(c in hex_digits for c in string)


def unknown_16(name):
    """Handler for region 16."""
    indices = {
        'bits_0_to_15':  (16, 32),
        'bits_16_to_23': (8, 16),  # only 0x28 seen thus far
        'bits_24_to_31': (0, 8)    # 0x24 & 0x6c seen here thus far
    }[name]
    __unknown_16 = get('unknown_16', 'binary')
    return __unknown_16[indices[0]: indices[1]]


def bootmode(name):
    """Handler for region 17."""
    indices = {
        'bit_0':         (31, 32),  # Unknown (Gordon hinted the Pi wouldn't boot with this set)
        'bit_1':         (30, 31),  # Sets the oscillator frequency to 19.2MHz
        'bit_2':         (29, 30),  # Unknown (Gordon hinted the Pi wouldn't boot with this set)
        'bit_3':         (28, 29),  # Enables pull ups on the SDIO pins
        'bits_4_to_18':  (13, 28),  # Unknown/Unused
        'bit_19':        (12, 13),  # Enables GPIO bootmode
        'bit_20':        (11, 12),  # Sets the bank to check for GPIO bootmode
        'bit_21':        (10, 11),  # Enables booting from SD card
        'bit_22':        (9, 10),   # Sets the bank to boot from (That's what Gordon said, Unclear)
        'bits_26_to_27': (7, 9),    # Unknown/Unused
        'bit_25':        (6, 7),    # Unknown (Is set on the Compute Module 3)
        'bits_23_to_24': (4, 6),    # Unknown/Unused
        'bit_28':        (3, 4),    # Enables USB device booting
        'bit_29':        (2, 3),    # Enables USB host booting (Ethernet and Mass Storage)
        'bits_30_31':    (0, 2)     # Unknown/Unused
    }[name]
    __bootmode = get('bootmode', 'binary')
    return __bootmode[indices[0]: indices[1]]


def unknown_27(name):
    """Handler for region 27."""
    indices = {
        'bits_0_to_15':  (16, 32),  # 5050 (1B, 2B 1.1), 7373 (2B 1.2), 2727(CM3), 1f1f (3B+)
        'bits_16_to_31': (0, 16)
    }[name]
    __unknown_27 = get('unknown_27', 'binary')
    return __unknown_27[indices[0]: indices[1]]


def revision(name):
    """Handler for region 30."""
    indices = {
        'legacy_board_revision': (27, 32),  # Region used to store the legacy revision
        'board_revision':        (28, 32),  # Revision of the board
        'board_type':            (20, 28),  # Model of the board
        'processor':             (16, 20),  # Installed Processor
        'manufacturer':          (12, 16),  # Manufacturer of the board
        'memory_size':           (9, 12),   # Amount of RAM the board has
        'new_flag':              (8, 9),    # If set, this board uses the new versioning scheme
        'bits_24_to_31':         (0, 8)     # Unused
    }[name]
    __revision = get('revision_number', 'binary')
    return __revision[indices[0]: indices[1]]


def overclock(name):
    """Handler for region 32."""
    indices = {
        'overvolt_protection': (31, 32),  # Overvolt protection bit
        'bits_0_to_30':        (0, 31)    # Unknown/Unused
    }[name]
    __overclock = get('overclock', 'binary')
    return __overclock[indices[0]: indices[1]]


def advanced_boot(name):
    """Handler for region 66."""
    indices = {
        'bits_0_to_6':   (25, 32),  # GPIO for ETH_CLK output pin
        'bit_7':         (24, 25),  # Enable ETH_CLK output pin
        'bits_8_to_14':  (17, 24),  # GPIO for LAN_RUN output pin
        'bit_15':        (16, 17),  # Enable LAN_RUN output pin
        'bits_16_to_23': (8, 16),   # Unknown/Unused
        'bit_24':        (7, 8),    # Extend USB HUB timeout parameter
        'bit_25':        (6, 7),    # ETH_CLK Frequency (0 = 25MHz, 1 = 24MHz)
        'bits_26_to_31': (0, 6)     # Unknown/Unused
    }[name]
    __advanced_boot = get('advanced_boot', 'binary')
    return __advanced_boot[indices[0]: indices[1]]


def process_bootmode():
    """Process bootmode, Check against the backup."""
    bootmode_primary = get('bootmode', 'binary')
    bootmode_copy = get('bootmode_copy', 'binary')
    if bootmode_primary != bootmode_copy:
        print('Bootmode fields are not the same, this is a bad thing!')


def process_serial():
    """Process Serial, Check against Inverse Serial."""
    serial = get('serial_number', 'hex')
    inverse_serial = get('serial_number_inverted', 'hex')
    try:
        if (int(serial, 16) ^ int(inverse_serial, 16)) != int('0xffffffff', 16):
            print('Serial failed checksum!')
    except TypeError:
        sys.exit('Serial number format invalid!')


def process_revision():
    """Process Revision, Handle depending on wether it's old or new style."""
    flag = revision('new_flag')
    if flag == '0':
        generate_info_legacy(revision('legacy_board_revision'))
    elif flag == '1':
        generate_info(revision('memory_size'),
                      revision('manufacturer'),
                      revision('processor'),
                      revision('board_type'),
                      revision('board_revision'))


def format_mac():
    """Format MAC Address in a human readable fashion."""
    mac_part_1 = get('mac_address_one', 'raw')
    mac_part_2 = get('mac_address_two', 'raw')
    if not mac_part_1 == '00000000':
        mac = mac_part_1 + mac_part_2
        return ':'.join(mac[i:i+2] for i in range(0, 12, 2))
    return 'None'


def process_hub_timeout(bit):
    """Return the HUB timeout."""
    if bit == '1':
        return '5 Seconds'
    return '2 Seconds'


def process_eth_clk_frequency(bit):
    """Return the ETH_CLK frequency."""
    if bit == '1':
        return '24MHz'
    return '25MHz'


def generate_info_legacy(bits):
    """Generate information for legacy board revision."""
    if bits in list(LEGACY_REVISIONS.keys()):
        input_dict = LEGACY_REVISIONS[bits]
    else:
        input_dict = LEGACY_REVISIONS['default']
    generate_info(MEMORY_SIZES[input_dict['memory_size']],
                  MANUFACTURERS[input_dict['manufacturer']],
                  PROCESSORS[input_dict['processor']],
                  BOARD_TYPES[input_dict['board_type']],
                  BOARD_REVISIONS[input_dict['board_revision']])


def generate_info(memory_size_in, manufacturer_in, processor_in, board_type_in, board_revision_in):
    """Generate information from board revision."""
    BOARD['memory'] = memory_size_in
    BOARD['manufacturer'] = manufacturer_in
    BOARD['processor'] = processor_in
    BOARD['type'] = board_type_in
    BOARD['revision'] = board_revision_in


def get(loc, specifier='raw'):
    """Get data from specified OTP region.
    Specifier determines whether it is returned 'raw', in 'binary', in 'octal', or in 'hex'adecmimal."""
    region = REGIONS[loc]
    if specifier == 'raw':
        return DATA[region]
    elif specifier == 'binary':
        return format(int(DATA[region], 16), '032b')
    elif specifier == 'hex':
        return format(int(DATA[region], 16), '#010x')
    elif specifier == 'octal':
        #TODO: Ask jas for more details on what she wants the octal output to look like.
        return format(int(DATA[region], 16), '#018o')
    else:
        raise ValueError("Invalid flag.")    

def pretty_string(value, do_binary=True):
    """Return a pretty OTP entry."""
    try:
        intval = int(value, 2)
        return '' + str(intval) + ' (' + hex(intval) + ') ' + (value if (do_binary) else '')
    except ValueError:
        sys.exit('Failed to make the string pretty!')


def read_otp():
    """Read OTP from specified file."""
    if len(sys.argv) > 1:  # We're given an argument on the command line
        if path.isfile(sys.argv[1]):
            with open(sys.argv[1], 'r') as file:
                __read_otp_inner(file)
        else:
            sys.exit('Unable to open file.')
    else:  # Use stdin instead.
        __read_otp_inner(sys.stdin)


def __read_otp_inner(myfile):
    """Inner part of OTP file reader."""
    for line in myfile:
        try:
            if "Command not registered" in line:
                raise TypoError
            try:
                region = int(line.split(':', 1)[0])
            except ValueError:
                sys.exit("Invalid OTP Dump (invalid region number '" + line.split(':', 1)[0] + "')")
            data = line.split(':', 1)[1][:8].rstrip('\r\n')

            try:
                if is_hex(data):
                    DATA[region] = data
                else:
                    raise ValueError("Reading region " + str(region) + ", string '" + data + "' is not hexadecimal.")
            except ValueError as exception:
                sys.exit('Invalid OTP Dump (' + str(exception) + ')')
        except IndexError:
            sys.exit('Invalid OTP Dump')
        except TypoError:
            sys.exit("Invalid OTP Dump. Please run 'vcgencmd otp_dump' to create file.")


read_otp()
process_bootmode()
process_serial()
process_revision()

print('  OTP Region 16 ( 0-23) :', pretty_string(unknown_16('bits_0_to_15')))
print('  OTP Region 16 (24-27) :', pretty_string(unknown_16('bits_16_to_23')))
print('  OTP Region 16 (28-31) :', pretty_string(unknown_16('bits_24_to_31')))
print('               Bootmode :', get('bootmode', 'hex'), get('bootmode', 'binary'))
print('        Bootmode - Copy :', get('bootmode_copy', 'hex'))
print('  OSC Frequency 19.2MHz :', bootmode('bit_1'))
print('    SDIO Pullup Enabled :', bootmode('bit_3'))
print('          GPIO Bootmode :', bootmode('bit_19'))
print('     GPIO Bootmode Bank :', bootmode('bit_20'))
print('        SD Boot Enabled :', bootmode('bit_21'))
print('              Boot Bank :', bootmode('bit_22'))
print('     OTP Region 17 (25) :', bootmode('bit_25'), '(This is Unknown but set on the CM3)')
print('USB Device Boot Enabled :', bootmode('bit_28'))
print('  USB Host Boot Enabled :', bootmode('bit_29'))
print('  OTP Region 27 ( 0-15) :', pretty_string(unknown_27('bits_0_to_15')))
print('  OTP Region 27 (16-31) :', pretty_string(unknown_27('bits_16_to_31')))
print('          Serial Number :', get('serial_number', 'hex'))
print('  Inverse Serial Number :', get('serial_number_inverted', 'hex'))
print('        Revision Number :', get('revision_number', 'hex'))
print('      New Revision Flag :', revision('new_flag'))
print('                    RAM :', MEMORY_SIZES_AS_STRING[BOARD['memory']], "MB")
print('           Manufacturer :', MANUFACTURERS_AS_STRING[BOARD['manufacturer']])
print('                    CPU :', PROCESSORS_AS_STRING[BOARD['processor']])
print('             Board Type :', 'Raspberry Pi Model ' + BOARD_TYPES_AS_STRING[BOARD['type']])
print('         Board Revision :', BOARD_REVISIONS_AS_STRING[BOARD['revision']])
print('           Batch Number :', get('batch_number', 'hex'))
print('Overvolt Protection Bit :', overclock('overvolt_protection'))
print('    Customer Region One :', get('customer_one', 'hex'))
print('    Customer Region Two :', get('customer_two', 'hex'))
print('  Customer Region Three :', get('customer_three', 'hex'))
print('   Customer Region Four :', get('customer_four', 'hex'))
print('   Customer Region Five :', get('customer_five', 'hex'))
print('    Customer Region Six :', get('customer_six', 'hex'))
print('  Customer Region Seven :', get('customer_seven', 'hex'))
print('  Customer Region Eight :', get('customer_eight', 'hex'))
print('  Codec License Key One :', get('codec_key_one', 'hex'))
print('  Codec License Key Two :', get('codec_key_two', 'hex'))
print('            MAC Address :', format_mac())
print('          Advanced Boot :', get('advanced_boot', 'hex'), get('advanced_boot', 'binary'))
print('     ETH_CLK Output Pin :', pretty_string(advanced_boot('bits_0_to_6'), False))
print(' ETH_CLK Output Enabled :', advanced_boot('bit_7'))
print('     LAN_RUN Output Pin :', pretty_string(advanced_boot('bits_8_to_14'), False))
print(' LAN_RUN Output Enabled :', advanced_boot('bit_15'))
print('        USB Hub Timeout :', process_hub_timeout(advanced_boot('bit_24')))
print('      ETH_CLK Frequency :', process_eth_clk_frequency(advanced_boot('bit_25')))
