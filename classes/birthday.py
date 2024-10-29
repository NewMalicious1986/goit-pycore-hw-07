from classes.field import Field
from datetime import datetime


class Birthday(Field):
    def __init__(self, value):
        try:
           date_obj = datetime.strptime(value, "%d.%m.%Y")
           self.value = date_obj
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")