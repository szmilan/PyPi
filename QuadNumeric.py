from Adafruit_LED_Backpack import HT16K33

# Digit value to bitmask mapping:
DIGIT_VALUES = {
    ' ': 0x00,
    '-': 0x40,
    '0': 0x3F,
    '1': 0x06,
    '2': 0x5B,
    '3': 0x4F,
    '4': 0x66,
    '5': 0x6D,
    '6': 0x7D,
    '7': 0x07,
    '8': 0x7F,
    '9': 0x6F,
    'A': 0x77,
    'B': 0x7C,
    'C': 0x39,
    'D': 0x5E,
    'E': 0x79,
    'F': 0x71
}

IDIGIT_VALUES = {
    ' ': 0x00,
    '-': 0x40,
    '0': 0x3F,
    '1': 0x30,
    '2': 0x5B,
    '3': 0x79,
    '4': 0x74,
    '5': 0x6D,
    '6': 0x6F,
    '7': 0x38,
    '8': 0x7F,
    '9': 0x7D,
    'A': 0x7E,
    'B': 0x67,
    'C': 0x0F,
    'D': 0x73,
    'E': 0x4F,
    'F': 0x4E
}



class QuadNumeric(HT16K33.HT16K33):
    """Seven segment 4 digit LED backpack display."""

    def __init__(self, invert=False, **kwargs):
        """Initialize display.  All arguments will be passed to the HT16K33 class
        initializer, including optional I2C address and bus number parameters.
        """
        super(QuadNumeric, self).__init__(**kwargs)
        self.invert = invert

    def set_invert(self, _invert):
        """Set whether the display is upside-down or not.
        """
        self.invert = _invert

    def set_digit_raw(self, pos, bitmask):
        """Set digit at position to raw bitmask value.  Position should be a value
        of 0 to 3 with 0 being the left most digit on the display."""
        if pos < 0 or pos > 3:
            # Ignore out of bounds digits.
            return

        # Calculate the correct position depending on orientation
        if self.invert:
            pos = 3-pos

        # Set the digit bitmask value at the appropriate position.
        self.buffer[pos*2] = bitmask & 0xFF


    def set_digit(self, pos, digit):
        """Set digit at position to provided value.  Position should be a value
        of 0 to 3 with 0 being the left most digit on the display.  Digit should
        be a number 0-9, character A-F, space (all LEDs off), or dash (-).
        """
        if self.invert:
            self.set_digit_raw(pos, IDIGIT_VALUES.get(str(digit).upper(), 0x00))
        else:
            self.set_digit_raw(pos, DIGIT_VALUES.get(str(digit).upper(), 0x00))


    def print_number_str(self, value, justify_right=True):
        """Print a 4 character long string of numeric values to the display.
        Characters in the string should be any supported character by set_digit.
        """
        # Calculate length
        length = len(value)

        # Error if value is longer than 4 characters.
        if length > 4:
            self.print_number_str('----')
            return
        # Calculcate starting position of digits based on justification.
        pos = (4-length) if justify_right else 0
        # Go through each character and print it on the display.
        for i, ch in enumerate(value):
            self.set_digit(pos, ch)
            pos += 1

    def print_float(self, value):
        """Print a numeric value in integer format.
        Value should be from 0 to 9999.
        """
        if not isinstance(value, (int, long, float, complex)):
            # Skip if value is not a number
            return
        if value < 0 or value > 9999:
            # Value out of range
            self.print_number_str('----')
        else:
            # Convert value to int and format to 4 digits
            self.print_number_str("{0:0=4d}".format(int(value)))


    def print_hex(self, value, justify_right=True):
        """Print a numeric value in hexadecimal.  Value should be from 0 to FFFF.
        """
        if value < 0 or value > 0xFFFF:
            # Ignore out of range values.
            return
        self.print_number_str('{0:X}'.format(value), justify_right)
