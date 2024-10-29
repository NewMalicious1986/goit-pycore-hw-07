from colorama import Fore, Style

from classes.address_book import AddressBook
from classes.record import Record

COMMANDS = """
    Available commands:
    - hello: Greet the assistant.
    - add <name> <phone>: Add a new contact.
    - change <name> <old_phone> <new_phone>: Change the phone number of a contact.
    - phone <name>: Get the phone number of a contact.
    - all: List all contacts.
    - add-birthday <name> <birthday>: Add a birthday to a contact.
    - show-birthday: <name> : Show the birthday of a contact.
    - birthdays: Show all birthdays.
    - help: List available commands.
    - close/exit: Close the assistant.
    """

COMMAND_NAMES = {
    "add": "add",
    "change": "change",
    "phone": "phone",
    "all": "all",
    "help": "help",
    "close": "close",
    "exit": "exit",
    "add-birthday": "add-birthday",
    "show-birthday": "show-birthday",
    "birthdays": "birthdays",
}


def input_error(command_name):
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                match command_name:
                    case "add":
                        return f"Error in '{command_name}' command: Give me a name and a phone number."
                    case "change":
                        return f"Error in '{command_name}' command: Give me a name and a phone number."
                    case "phone":
                        return f"Error in '{command_name}' command: Enter user nam."
                    case "add-birthday":
                        return f"Error in '{command_name}' command: Enter user name and birthday."
                    case "show-birthday":
                        return f"Error in '{command_name}' command: Enter user name."
                    case _:
                        return f"Error in '{command_name}' command: Invalid input."
            except IndexError:
                return (
                    f"Error in '{command_name}' command: Not enough arguments provided."
                )
            except KeyError:
                return (
                    f"Error in '{command_name}' command: Contact {args[0]} not found."
                )

        return inner

    return decorator


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error(COMMAND_NAMES["add"])
def add_contact(args, book: AddressBook):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)


@input_error(COMMAND_NAMES["change"])
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)


@input_error(COMMAND_NAMES["phone"])
def get_phone(args, book: AddressBook):
    name = args[0]
    record: Record = book.find(name)
    phones = record.get_all_phones()
    print(f"Phones of {name}:")
    print("\n".join(phone.value for phone in phones))


def get_all_contacts(book: AddressBook):
    for record in book.data.values():
        print(record)


@input_error(COMMAND_NAMES["add-birthday"])
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        print(f"Birthday {birthday} added to {name}.")
    else:
        print(f"Contact {name} not found.")


@input_error(COMMAND_NAMES["show-birthday"])
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        birthday = record.show_birthdays()
        print(f"{name}'s birthday: {birthday}")
    else:
        print(f"Contact {name} not found.")


def birthdays(book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if len(upcoming) > 0:
        print("Upcoming birthdays:")
        for birthday in upcoming:
            print(f"{birthday['name']}: {birthday['next_upcoming_birthday']}")
    else:
        print("No upcoming birthdays.")


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input(f"{Style.RESET_ALL}Enter a command: ")
        command, *args = parse_input(user_input)
        if command in COMMAND_NAMES:
            match command:
                case "close" | "exit":
                    print("Good bye!")
                    break
                case "hello":
                    print("How can I help you?")
                case "add":
                    add_contact(args, book)
                case "change":
                    print(change_contact(args, book))
                case "phone":
                    print(get_phone(args, book))
                case "all":
                    get_all_contacts(book)
                case "add-birthday":
                    add_birthday(args, book)
                case "show-birthday":
                    show_birthday(args, book)
                case "birthdays":
                    birthdays(book)
                case "help":
                    print(COMMANDS)
        else:
            print(
                f"{Fore.RED}Invalid command.\n{Style.RESET_ALL}To see all commands available type 'help'"
            )


if __name__ == "__main__":
    main()
