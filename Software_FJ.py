# Student: Juan Camilo Peláez Feged
# Grupo: 213023_37
# SOFTWARE FJ - Customer, Services and Reservations Management System



# IMPORTS

import tkinter as tk
from tkinter import ttk, messagebox

from abc import ABC, abstractmethod

from datetime import datetime

# LOGGER

def write_log(message):

    try:

        with open(
            "Software_FJ_logs.txt",
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                f"{datetime.now()} - {message}\n"
            )

    except Exception as error:

        print("Log Error:", error)

# CUSTOM EXCEPTIONS

class SystemError(Exception):
    pass


class InvalidCustomerError(SystemError):
    pass


class InvalidServiceError(SystemError):
    pass


class InvalidReservationError(SystemError):
    pass


class OperationNotAllowedError(SystemError):
    pass

# ABSTRACT CLASS

class Entity(ABC):

    def __init__(self, id):

        self._id = id

    @property
    def id(self):

        return self._id

    @abstractmethod
    def display(self):

        pass

# CUSTOMER CLASS

class Customer(Entity):

    def __init__(self, id, name, email, phone):

        super().__init__(id)

        self.__validate_name(name)
        self.__validate_email(email)
        self.__validate_phone(phone)

        self.__name = name
        self.__email = email
        self.__phone = phone


    # VALIDATIONS

    def __validate_name(self, name):

        if name.strip() == "":

            raise InvalidCustomerError(
                "Customer name cannot be empty."
            )


    def __validate_email(self, email):

        if "@" not in email or "." not in email:

            raise InvalidCustomerError(
                "Invalid email address."
            )


    def __validate_phone(self, phone):

        if not phone.isdigit():

            raise InvalidCustomerError(
                "Phone must contain only numbers."
            )

        if len(phone) != 10:

            raise InvalidCustomerError(
                "Phone must have 10 digits."
            )


    # PROPERTIES

    @property
    def name(self):

        return self.__name


    @property
    def email(self):

        return self.__email


    @property
    def phone(self):

        return self.__phone


    # POLYMORPHISM

    def display(self):

        return (
            f"ID: {self.id} | "
            f"Name: {self.name} | "
            f"Email: {self.email} | "
            f"Phone: {self.phone}"
        )

# SERVICE CLASS

class Service(Entity, ABC):
    pass

# ROOM RESERVATION

class RoomReservation(Service):
    pass

# EQUIPMENT RENTAL

class EquipmentRental(Service):
    pass

# CONSULTING SERVICE

class ConsultingService(Service):
    pass

# RESERVATION CLASS

class Reservation:
    pass

# LISTS



# FUNCTIONS



# TKINTER INTERFACE



# MAIN

if __name__ == "__main__":

    try:

        customer = Customer(
            1,
            "Juan Camilo",
            "juan@gmail.com",
            "3001234567"
        )

        print(customer.display())

    except Exception as error:

        print(error)