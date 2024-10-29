import re

from classes.field import Field

pattern = r"^\d{10}$"


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if re.match(pattern, value):
            self.value = value
        else:
            self.value = None
            print("Invalid phone number. Please enter a 10-digit number.")

    pass
