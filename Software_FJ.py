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

    _next_id = 1

    def __init__(self):

        self._id = Entity._next_id
        Entity._next_id += 1


    @property
    def id(self):

        return self._id


    @abstractmethod
    def display(self):

        pass

# CUSTOMER CLASS

class Customer(Entity):

    def __init__(self, name, email, phone):

        super().__init__()

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

    def __init__(self, name, price):

        super().__init__()

        self.__validate_price(price)

        self.__name = name
        self.__price = price


    # VALIDATIONS

    def __validate_price(self, price):

        if price <= 0:

            raise InvalidServiceError(
                "Service price must be greater than zero."
            )


    # PROPERTIES

    @property
    def name(self):

        return self.__name


    @property
    def price(self):

        return self.__price


    # POLYMORPHISM

    def display(self):

        return (
            f"ID: {self.id} | "
            f"Service: {self.name} | "
            f"Price: ${self.price}"
        )


    @abstractmethod
    def description(self):

        pass


    @abstractmethod
    def calculate_cost(self):

        pass

# ROOM RESERVATION

class RoomReservation(Service):

    def __init__(self, name, price):

        super().__init__(name, price)


    # POLYMORPHISM

    def description(self):

        return (
            f"Room Reservation - "
            f"${self.price} per hour"
        )


    # METHOD OVERLOADING (Optional parameters)

    def calculate_cost(
            self,
            hours=1,
            tax=False
    ):

        if hours <= 0:

            raise InvalidServiceError(
                "Hours must be greater than zero."
            )


        total = self.price * hours


        if tax:

            total *= 1.19


        return total

# EQUIPMENT RENTAL

class EquipmentRental(Service):

    def __init__(self, name, price):

        super().__init__(name, price)


    # POLYMORPHISM

    def description(self):

        return (
            f"Equipment Rental - "
            f"${self.price} per day"
        )


    # METHOD OVERLOADING (Optional parameters)

    def calculate_cost(
            self,
            days=1,
            discount=0
    ):

        if days <= 0:

            raise InvalidServiceError(
                "Days must be greater than zero."
            )


        if discount < 0 or discount > 1:

            raise InvalidServiceError(
                "Invalid discount."
            )


        total = self.price * days

        total -= total * discount

        return total

# CONSULTING SERVICE

class ConsultingService(Service):

    def __init__(self, name, price):

        super().__init__(name, price)


    # POLYMORPHISM

    def description(self):

        return (
            f"Specialized Consulting - "
            f"${self.price} per hour"
        )


    # METHOD OVERLOADING (Optional parameters)

    def calculate_cost(
            self,
            hours=1,
            extra_fee=0
    ):

        if hours <= 0:

            raise InvalidServiceError(
                "Hours must be greater than zero."
            )


        total = (self.price * hours) + extra_fee

        return total

# RESERVATION CLASS

class Reservation:

    def __init__(
            self,
            customer,
            service,
            duration
    ):

        if duration <= 0:

            raise InvalidReservationError(
                "Duration must be greater than zero."
            )

        self.customer = customer
        self.service = service
        self.duration = duration
        self.status = "Pending"


    def confirm(self):

        self.status = "Confirmed"

        write_log(
            f"Reservation confirmed for {self.customer.name}"
        )


    def cancel(self):

        self.status = "Cancelled"

        write_log(
            f"Reservation cancelled for {self.customer.name}"
        )


    def process(self):

        try:

            total = self.service.calculate_cost(
                self.duration
            )

        except Exception as error:

            write_log(
                f"Reservation Error: {error}"
            )

            raise InvalidReservationError(
                "Reservation could not be processed."
            ) from error

        else:

            write_log(
                f"Reservation processed successfully."
            )

            return total

        finally:

            write_log(
                "Reservation process finished."
            )


    def display(self):

        return (

            f"Customer: {self.customer.name} | "
            f"Service: {self.service.name} | "
            f"Status: {self.status}"

        )

# LISTS



# FUNCTIONS



# TKINTER INTERFACE



# MAIN

if __name__ == "__main__":

    print("Software FJ started successfully.")