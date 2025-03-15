"""
Технiчний опис завдання

Розробіть систему для управління адресною книгою.
Сутності:

Field: Базовий клас для полів запису.
Name: Клас для зберігання імені контакту. Обов'язкове поле.
Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
Record: Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
AddressBook: Клас для зберігання та управління записами.

Функціональність:

AddressBook:Додавання записів.
Пошук записів за іменем.
Видалення записів за іменем.
Record:Додавання телефонів.
Видалення телефонів.
Редагування телефонів.
Пошук телефону.
"""
"""
===================================================================>
Field — базовий клас для всіх полів, він зберігає значення та перевизначає метод __str__ для виведення значення.

Name — клас для імені контакту. Він перевіряє, чи не є значення порожнім.

Phone — клас для номера телефону з валідацією. Метод validate_phone перевіряє, чи складається телефон з 10 цифр.

Record — клас для кожного контакту. Він дозволяє додавати, видаляти, редагувати телефони і шукати їх. Також він містить метод __str__ для виведення контактів у зручному форматі.

AddressBook — клас для управління контактами, що зберігає контакти в словнику (UserDict). Він підтримує методи для додавання, видалення і пошуку записів.
"""
"""
====================================================================>
При виклику print(book) Python викликає метод __str__ класу AddressBook.
У методі __str__ класу AddressBook є генератор, який перебирає всі об'єкти Record в словнику self.data. Для кожного запису викликається str(record), що фактично викликає метод __str__ класу Record.
Це дозволяє вивести список всіх контактів у вигляді, який визначений в методі __str__ класу Record.
"""

from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        try:
            if not self.validate_phone(value):
                raise ValueError(f"Invalid phone number format: {value}")
            super().__init__(value)
        except ValueError as e:
            print(f"Error: {e}")
            self.value = None

    @staticmethod
    def validate_phone(value):
        return bool(re.match(r"^\d{10}$", value))

class Record:
    def __init__(self, name):
        try:
            self.name = Name(name)
        except ValueError as e:
            print(f"Error: {e}")
            self.name = None
        self.phones = []

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except ValueError as e:
            print(f"Error: {e}")

    def delete_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        try:
            for p in self.phones:
                if p.value == old_phone:
                    self.delete_phone(old_phone)
                    self.add_phone(new_phone)
                    return
            raise ValueError(f"Phone number {old_phone} not found.")
        except ValueError as e:
            print(f"Error: {e}")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def __str__(self):
        if self.name is None:
            return "Invalid contact name"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones if p.value)}"

class AddressBook(UserDict):
    def add_record(self, record):
        if record.name is None:
            print("Cannot add a record with an invalid name.")
            return
        self.data[record.name.value] = record
        # print("self.data", self.data)

    def find(self, name):
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            print(f"Error: Record for {name} not found.")

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
# Спроба додати недійсний номер телефону
john_record.add_phone("55555555f5")  # Потрібно отримати повідомлення про помилку
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
print("All records in the book:")
print(book)

# Знаходження та редагування телефону для John
john = book.find("John")
if john:
    john.edit_phone("1234567890", "1112223333")

print("\nAfter editing John's phone:")
print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"\nFound phone in John's record: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
print("\nAfter deleting Jane's record:")
print(book)  # Виведення всіх записів, зокрема John

