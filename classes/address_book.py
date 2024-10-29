from collections import UserDict
from datetime import datetime, timedelta
from classes.record import Record

DATE_FORMAT = "%d.%m.%Y"
DAYS_IN_WEEK = 7
WEEKEND_DAYS = [5, 6]  # Saturday and Sunday

class AddressBook(UserDict):
    def add_record(self, record: Record):
        if not self.data.get(record.name.value):
            self.data[record.name.value] = record
            print(f"Contact {record.name.value} added.")
        else:
            self.data[record.name.value].add_phone(record.phones[0].value)
            print(f"Phone number {record.phones[0].value} add to the contact {record.name.value}.")

    def find(self, name: str):
        return self.data.get(name, None)

    def delete(self, name):
        try:
            self.data.pop(name)
        except KeyError:
            print(f"Contact {name} not found.")

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming_birthdays = []

        for user in self.data.values():
            birthday_this_year = (
                user.birthday.value
                .date()
                .replace(year=today.year)
            )
            days_until_birthday = (birthday_this_year - today).days

            if 0 <= days_until_birthday <= DAYS_IN_WEEK:
                if birthday_this_year.weekday() in WEEKEND_DAYS:
                    birthday_this_year += timedelta(days=(7 - birthday_this_year.weekday()))

                upcoming_birthdays.append(
                    {
                        "name": user.name.value,
                        "next_upcoming_birthday": birthday_this_year.strftime(DATE_FORMAT),
                    }
                )

        return upcoming_birthdays
