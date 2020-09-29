"""Controls Control4 Light devices.
"""


class C4Light:
    def __init__(self, C4Director, item_id):
        """Creates a Control4 Light object.

        Parameters:
            `C4Director` - A `pyControl4.director.C4Director` object that corresponds to the Control4 Director that the light is connected to.

            `item_id` - The Control4 item ID of the light.
        Light varis:
            {
                "type": "color",
                "value": {
                    "m": -1,
                    "m": 1,
                    "l": 100,
                    "w": 0,
                    "s": 0
                },
                "other": null,
                "detail": {
                    "type": 5,
                    "set": {
                        "s": "1",
                        "m": null
                    },
                    "mode": {
                        "11": "跳舞",
                        "12": "彩色呼吸",
                        "13": "彩色跳变",
                        "14": "七彩变幻",
                        "15": "七彩跳变"
                    }
                },
                "attr": {
                    "ID": "13",
                    "DEVID": "5",
                    "NAME": "小灯",
                    "SYSNAME": "color",
                    "ICON": "cd",
                    "YYBM": null,
                    "INUSE": "1",
                    "CANDEL": "0",
                    "ISR": "1",
                    "ISS": "0",
                    "ISC": "1"
                },
                "phydev": "1"
            }
        """
        self.director = C4Director
        self.item_id = item_id

    async def get_level(self):
        """Returns the level of a dimming-capable light as an int 0-100.
        Will cause an error if called on a non-dimmer switch. Use `getState()` instead.
        """
        value = await self.director.get_item_variable_value(self.item_id, "l")
        return int(value)

    async def get_state(self):
        """Returns the power state of a dimmer or switch as a boolean (True=on, False=off).
        """
        value = await self.director.get_item_variable_value(self.item_id, "m")
        if value == "-1":
            return False
        else:
            return True

    async def set_level(self, level):
        """Sets the light level of a dimmer or turns on/off a switch.
        Any `level > 0` will turn on a switch, and `level = 0` will turn off a switch.

        Parameters:
            `level` - (int) 0-100
        """
        data = {
            "rs": "execAttr",
            "rsargs[]": self.item_id,
            "rsargs[1][m]": "1",
            "rsargs[1][l]": level,
            "rsargs[1][w]": "0",
            "rsargs[1][s]": "0"
        }
        await self.director.request(uri="/devattr/devattr.php", params=data)

    async def turn_on(self):
        """turns on a light.
        """
        data = {
            "rs": "execAttr",
            "rsargs[]": self.item_id,
            "rsargs[1][m]": "0",
        }
        await self.director.request(uri="/devattr/devattr.php", params=data)

    async def turn_off(self):
        """turns off a light.
        """
        data = {
            "rs": "execAttr",
            "rsargs[]": self.item_id,
            "rsargs[1][m]": "-1",
        }
        await self.director.request(uri="/devattr/devattr.php", params=data)