import pickle


from datetime import datetime, timedelta
from collections import UserDict
import re
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
def main():
    # Завантаження даних з файлу
    book = load_data()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            # Збереження даних перед виходом
            save_data(book)
            print("Data saved. Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all_contacts(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(show_upcoming_birthdays(args, book))

        else:
            print("Invalid command.")
class AddressBook(UserDict):
    def add_record(self, record):
        if not isinstance(record, Record):
            raise TypeError("Only Record instances can be added.")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Contact not found.")

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                next_birthday = birthday_date.replace(year=today.year)
                
                if today <= next_birthday <= today + timedelta(days=7):
                    if next_birthday.weekday() >= 5:
                        next_birthday += timedelta(days=(7 - next_birthday.weekday()))
                    upcoming_birthdays.append({"name": record.name.value, "birthday": next_birthday.strftime('%d.%m.%Y')})

        return upcoming_birthdays

    def __str__(self):
        if self.data:
            return "\n".join(str(record) for record in self.data.values())
        else:
            return "No contacts found."