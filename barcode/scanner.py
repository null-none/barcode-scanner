import usb.core
import usb.util

VENDOR_ID = 0x05F9
PRODUCT_ID = 0x2203


class USB(object):
    def __init__(self, vendor_id=VENDOR_ID, product_id=PRODUCT_ID):
        self.device = usb.core.find(idVendor=vendor_id, idProduct=product_id)
        if self.device is None:
            raise ValueError("USB device not found")
        self.needs_reattach = False
        if self.device.is_kernel_driver_active(0):
            self.needs_reattach = True
            self.device.detach_kernel_driver(0)
            print("Detached USB device from kernel driver")

        self.device.set_configuration()
        cfg = self.device.get_active_configuration()
        intf = cfg[(0, 0)]
        self.ep = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
            == usb.util.ENDPOINT_IN,
        )

    def __del__(self):
        self.device.reset()

    def hid2ascii(self, lst):
        """The USB HID device sends an 8-byte code for every character. This
        routine converts the HID code to an ASCII character.

        See https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf
        for a complete code table. Only relevant codes are used here."""

        # Example input from scanner representing the string "http:":
        #   array('B', [0, 0, 11, 0, 0, 0, 0, 0])   # h
        #   array('B', [0, 0, 23, 0, 0, 0, 0, 0])   # t
        #   array('B', [0, 0, 0, 0, 0, 0, 0, 0])    # nothing, ignore
        #   array('B', [0, 0, 23, 0, 0, 0, 0, 0])   # t
        #   array('B', [0, 0, 19, 0, 0, 0, 0, 0])   # p
        #   array('B', [2, 0, 51, 0, 0, 0, 0, 0])   # :

        assert len(lst) == 8, "Invalid data length (needs 8 bytes)"
        conv_table = {
            0: ["", ""],
            4: ["a", "A"],
            5: ["b", "B"],
            6: ["c", "C"],
            7: ["d", "D"],
            8: ["e", "E"],
            9: ["f", "F"],
            10: ["g", "G"],
            11: ["h", "H"],
            12: ["i", "I"],
            13: ["j", "J"],
            14: ["k", "K"],
            15: ["l", "L"],
            16: ["m", "M"],
            17: ["n", "N"],
            18: ["o", "O"],
            19: ["p", "P"],
            20: ["q", "Q"],
            21: ["r", "R"],
            22: ["s", "S"],
            23: ["t", "T"],
            24: ["u", "U"],
            25: ["v", "V"],
            26: ["w", "W"],
            27: ["x", "X"],
            28: ["y", "Y"],
            29: ["z", "Z"],
            30: ["1", "!"],
            31: ["2", "@"],
            32: ["3", "#"],
            33: ["4", "$"],
            34: ["5", "%"],
            35: ["6", "^"],
            36: ["7", "&"],
            37: ["8", "*"],
            38: ["9", "("],
            39: ["0", ")"],
            40: ["\n", "\n"],
            41: ["\x1b", "\x1b"],
            42: ["\b", "\b"],
            43: ["\t", "\t"],
            44: [" ", " "],
            45: ["_", "_"],
            46: ["=", "+"],
            47: ["[", "{"],
            48: ["]", "}"],
            49: ["\\", "|"],
            50: ["#", "~"],
            51: [";", ":"],
            52: ["'", '"'],
            53: ["`", "~"],
            54: [",", "<"],
            55: [".", ">"],
            56: ["/", "?"],
            100: ["\\", "|"],
            103: ["=", "="],
        }

        # A 2 in first byte seems to indicate to shift the key. For example
        # a code for ';' but with 2 in first byte really means ':'.
        if lst[0] == 2:
            shift = 1
        else:
            shift = 0

        # The character to convert is in the third byte
        ch = lst[2]
        if ch not in conv_table:
            print("Warning: data not in conversion table")
            return ""
        return conv_table[ch][shift]

    def get_code(self):
        # Wait up to 0.5 seconds for data. 500 = 0.5 second timeout.
        data = self.ep.read(1000, 500)
        return self.hid2ascii(data)
