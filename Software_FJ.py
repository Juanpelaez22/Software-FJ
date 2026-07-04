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
    pass

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