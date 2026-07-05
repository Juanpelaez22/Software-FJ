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

        self.__validate_name(name)
        self.__validate_price(price)
        self.__name = name
        self.__price = price


    # VALIDATIONS

    def __validate_name(self, name):

        if name.strip() == "":

            raise InvalidServiceError(
                "Service name cannot be empty."
            )


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
# Internal lists used to store system information

customers = []

services = []

reservations = []

# FUNCTIONS 

## CURSTOMER FUNCTIONS

def add_customer(customer):

    for item in customers:
        if item.email == customer.email:
            raise InvalidCustomerError(
                "Email already registered."
            )

    customers.append(customer)

    write_log(
        f"Customer added: {customer.name}"
    )


def find_customer(customer_id):
    for customer in customers:
        if customer.id == customer_id:

            return customer

    return None

def find_customer_by_name(name):

    for customer in customers:
        if customer.name == name:

            return customer

    return None


def delete_customer(customer_id):

    customer = find_customer(customer_id)

    if customer is None:
        raise InvalidCustomerError(
            "Customer not found."
        )

    customers.remove(customer)

    write_log(
        f"Customer deleted: {customer.name}"
    )


def display_customers():
    for customer in customers:
        print(customer.display())





## SERVICE FUNCTIONS

def add_service(service):

    for item in services:

        if item.name.lower() == service.name.lower():

            raise InvalidServiceError(
                "Service already exists."
            )

    services.append(service)

    write_log(
        f"Service added: {service.name}"
    )


def find_service(service_id):

    for service in services:

        if service.id == service_id:

            return service

    return None

def find_service_by_name(name):

    for service in services:

        if service.name == name:

            return service

    return None

def delete_service(service_id):

    service = find_service(service_id)
    if service is None:
        raise InvalidServiceError(
            "Service not found."
        )

    services.remove(service)

    write_log(
        f"Service deleted: {service.name}"
    )


def display_services():

    for service in services:
        print(service.display())

## RESERVATION FUNCTIONS

def create_reservation(customer, service, duration):

    reservation = Reservation(
        customer,
        service,
        duration
    )

    reservations.append(reservation)

    write_log(
        f"Reservation created for {customer.name}"
    )

    return reservation


def confirm_reservation(reservation):
    reservation.confirm()


def cancel_reservation(reservation):
    reservation.cancel()


def process_reservation(reservation):
    return reservation.process()


def display_reservations():

    for reservation in reservations:

        print(reservation.display())

def find_reservation(customer_name, service_name):

    for reservation in reservations:
        if (
            reservation.customer.name == customer_name
            and
            reservation.service.name == service_name
        ):
            return reservation

    return None        


# TKINTER FUNCTIONS



def add_customer_interface():

    try:
        customer = Customer(

            entry_name.get(),
            entry_email.get(),
            entry_phone.get()

        )

        add_customer(customer)

        refresh_customer_table()

        update_customer_combobox()

        
        entry_name.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_phone.delete(0, tk.END)

        messagebox.showinfo(
            "Success",
            "Customer added successfully."
        )

    except Exception as error:

        write_log(str(error))

        messagebox.showerror(
            "Error",
            str(error)
        )


def delete_customer_interface():

    try:

        selected = customer_table.selection()

        if not selected:
            raise InvalidCustomerError(
                "Please select a customer."
            )

        values = customer_table.item(
            selected[0]
        )["values"]

        customer_id = values[0]

        delete_customer(customer_id)

        refresh_customer_table()

        update_customer_combobox()

        messagebox.showinfo(

            "Success",
            "Customer deleted successfully."

        )

    except Exception as error:

        write_log(str(error))

        messagebox.showerror(
            "Error",
            str(error)

        )


def refresh_customer_table():

    customer_table.delete(*customer_table.get_children())

    for customer in customers:
        customer_table.insert(
            "",
            "end",
            values=(
                customer.id,
                customer.name,
                customer.email,
                customer.phone
            )

        )


def refresh_service_table():

    service_table.delete(*service_table.get_children())

    for service in services:

        service_table.insert(
            "",
            "end",
            values=(
                service.id,
                service.description(),
                service.name,
                service.price
            )

        )


def update_service_combobox():

    combo_reservation_service["values"] = [
        service.name
        for service in services

    ]

def refresh_reservation_table():

    reservation_table.delete(*reservation_table.get_children())

    for reservation in reservations:
        reservation_table.insert(
            "",
            "end",
            values=(
                reservation.customer.name,
                reservation.service.name,
                reservation.duration,
                reservation.status
            )

        )    


def create_reservation_interface():

    try:

        customer = find_customer_by_name(
            combo_customer.get()
        )

        service = find_service_by_name(
            combo_reservation_service.get()
        )

        duration = int(
            entry_duration.get()
        )

        create_reservation(
            customer,
            service,
            duration
        )

        refresh_reservation_table()

        entry_duration.delete(0, tk.END)

        messagebox.showinfo(
            "Success",
            "Reservation created successfully."
        )

    except Exception as error:

        write_log(str(error))

        messagebox.showerror(
            "Error",
            str(error)

        )


def confirm_reservation_interface():

    try:

        selected = reservation_table.selection()

        if not selected:
            raise InvalidReservationError(
                "Please select a reservation."
            )

        values = reservation_table.item(
            selected[0]
        )["values"]

        reservation = find_reservation(
            values[0],
            values[1]
        )

        confirm_reservation(reservation)

        refresh_reservation_table()

        messagebox.showinfo(

            "Success",
            "Reservation confirmed successfully."

        )

    except Exception as error:

        write_log(str(error))

        messagebox.showerror(

            "Error",
            str(error)

        )

def cancel_reservation_interface():

    try:

        selected = reservation_table.selection()

        if not selected:
            raise InvalidReservationError(
                "Please select a reservation."
            )

        values = reservation_table.item(
            selected[0]
        )["values"]

        reservation = find_reservation(
            values[0],
            values[1]
        )

        cancel_reservation(reservation)

        refresh_reservation_table()

        messagebox.showinfo(

            "Success",
            "Reservation cancelled successfully."

        )

    except Exception as error:

        write_log(str(error))

        messagebox.showerror(

            "Error",
            str(error)

        )

def add_service_interface():

    try:
        service_type = combo_service.get()
        name = entry_service_name.get()
        price = float(entry_service_price.get())
        if service_type == "Room Reservation":
            service = RoomReservation(
                name,
                price
            )

        elif service_type == "Equipment Rental":

            service = EquipmentRental(
                name,
                price
            )

        else:
            service = ConsultingService(
                name,
                price
            )

        add_service(service)

        refresh_service_table()

        update_service_combobox()

        entry_service_name.delete(0, tk.END)
        entry_service_price.delete(0, tk.END)

        messagebox.showinfo(
            "Success",
            "Service added successfully."
        )

    except Exception as error:

        write_log(str(error))

        messagebox.showerror(
            "Error",
            str(error)
        )    

def delete_service_interface():

    try:

        selected = service_table.selection()
        if not selected:
            raise InvalidServiceError(
                "Please select a service."
            )

        values = service_table.item(
            selected[0]
        )["values"]

        service_id = values[0]

        delete_service(service_id)

        refresh_service_table()

        update_service_combobox()

        messagebox.showinfo(

            "Success",

            "Service deleted successfully."

        )

    except Exception as error:

        write_log(str(error))

        messagebox.showerror(

            "Error",

            str(error)

        )        

def update_customer_combobox():

    combo_customer["values"] = [
        customer.name
        for customer in customers

    ]


# TKINTER INTERFACE
root = tk.Tk()

root.title("Software FJ Management System")

root.geometry("900x400")

root.resizable(False, False)

title_label = tk.Label(
    root,
    text="SOFTWARE FJ MANAGEMENT SYSTEM",
    font=("Arial", 16, "bold")
)

title_label.pack(pady=10)

# NOTEBOOK

notebook = ttk.Notebook(root)

notebook.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

customers_tab = tk.Frame(notebook)
services_tab = tk.Frame(notebook)
reservations_tab = tk.Frame(notebook)

notebook.add(
    customers_tab,
    text="Customers"
)

notebook.add(
    services_tab,
    text="Services"
)

notebook.add(
    reservations_tab,
    text="Reservations"
)


customer_frame = tk.LabelFrame(
    customers_tab,
    text="Customers",
    padx=10,
    pady=10
)

customer_frame.pack(
    fill="x",
    padx=10,
    pady=10
)

# Name

tk.Label(customer_frame, text="Name:").grid(
    row=0,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

entry_name = tk.Entry(customer_frame, width=25)
entry_name.grid(row=0, column=1, padx=5)

# Email

tk.Label(customer_frame, text="Email:").grid(
    row=0,
    column=2,
    padx=5,
    sticky="w"
)

entry_email = tk.Entry(customer_frame, width=25)
entry_email.grid(row=0, column=3, padx=5)

# Phone

tk.Label(customer_frame, text="Phone:").grid(
    row=0,
    column=4,
    padx=5,
    sticky="w"
)

entry_phone = tk.Entry(customer_frame, width=18)
entry_phone.grid(row=0, column=5, padx=5)


button_add_customer = tk.Button(

    customer_frame,
    text="Add Customer",
    width=15,
    command=add_customer_interface

)

button_add_customer.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


button_delete_customer = tk.Button(

    customer_frame,
    text="Delete Customer",
    width=15,
    command=delete_customer_interface

)

button_delete_customer.grid(
    row=1,
    column=3,
    padx=10,
    pady=10
)

customer_table = ttk.Treeview(

    customer_frame,
    columns=("ID", "Name", "Email", "Phone"),
    show="headings",
    height=4

)

customer_table.heading("ID", text="ID")
customer_table.heading("Name", text="Name")
customer_table.heading("Email", text="Email")
customer_table.heading("Phone", text="Phone")

customer_table.column("ID", width=60)
customer_table.column("Name", width=220)
customer_table.column("Email", width=320)
customer_table.column("Phone", width=180)

customer_table.grid(

    row=2,
    column=0,
    columnspan=8,
    padx=10,
    pady=10,
    sticky="ew"
)

# SERVICES SECTION
service_frame = tk.LabelFrame(
    services_tab,
    text="Services",
    padx=10,
    pady=10
)

service_frame.pack(
    fill="x",
    padx=10,
    pady=10
)

tk.Label(
    service_frame,
    text="Type:"
).grid(row=0, column=0, padx=5, pady=5)

combo_service = ttk.Combobox(
    service_frame,
    values=[
        "Room Reservation",
        "Equipment Rental",
        "Consulting Service"
    ],
    width=22,
    state="readonly"
)

combo_service.grid(row=0, column=1)

combo_service.current(0)

# Service name
tk.Label(
    service_frame,
    text="Name:"
).grid(row=0, column=2, padx=5)

entry_service_name = tk.Entry(
    service_frame,
    width=25
)

entry_service_name.grid(row=0, column=3)

# Service price
tk.Label(
    service_frame,
    text="Price:"
).grid(row=0, column=4, padx=5)

entry_service_price = tk.Entry(
    service_frame,
    width=15
)

entry_service_price.grid(row=0, column=5)

# Add Service Button
button_add_service = tk.Button(

    service_frame,
    text="Add Service",
    width=15,
    command=add_service_interface

)

button_add_service.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)

button_delete_service = tk.Button(

    service_frame,
    text="Delete Service",
    width=15,
    command=delete_service_interface
)

button_delete_service.grid(
    row=1,
    column=3,
    padx=10,
    pady=10
)

# Service Table
service_table = ttk.Treeview(

    service_frame,
    columns=("ID", "Type", "Name", "Price"),
    show="headings",
    height=4

)

service_table.heading("ID", text="ID")
service_table.heading("Type", text="Type")
service_table.heading("Name", text="Name")
service_table.heading("Price", text="Price")

service_table.column("ID", width=60)
service_table.column("Type", width=200)
service_table.column("Name", width=220)
service_table.column("Price", width=120)

service_table.grid(
    row=2,
    column=0,
    columnspan=8,
    padx=10,
    pady=10,
    sticky="ew"
)

# RESERVATIONS SECTION
reservation_frame = tk.LabelFrame(
    reservations_tab,
    text="Reservations",
    padx=10,
    pady=10
)

reservation_frame.pack(
    fill="x",
    padx=10,
    pady=10
)

# Customer selection
tk.Label(
    reservation_frame,
    text="Customer:"
).grid(row=0, column=0, padx=5, pady=5)

combo_customer = ttk.Combobox(
    reservation_frame,
    width=25,
    state="readonly"
)

combo_customer.grid(row=0, column=1)

# Service selection
tk.Label(
    reservation_frame,
    text="Service:"
).grid(row=0, column=2, padx=5)

combo_reservation_service = ttk.Combobox(
    reservation_frame,
    width=25,
    state="readonly"
)

combo_reservation_service.grid(row=0, column=3)

# Duration input
tk.Label(
    reservation_frame,
    text="Duration:"
).grid(row=0, column=4, padx=5)

entry_duration = tk.Entry(
    reservation_frame,
    width=10
)

entry_duration.grid(row=0, column=5)

# Buttons for reservation actions
button_create_reservation = tk.Button(

    reservation_frame,
    text="Create Reservation",
    width=18,
    command=create_reservation_interface

)

button_create_reservation.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)

button_confirm = tk.Button(

    reservation_frame,
    text="Confirm",
    width=12,
    command=confirm_reservation_interface

)

button_confirm.grid(
    row=1,
    column=2,
    padx=10
)

button_cancel = tk.Button(
    reservation_frame,
    text="Cancel",
    width=12,
    command=cancel_reservation_interface

)

button_cancel.grid(
    row=1,
    column=3,
    padx=10
)

# Reservation Table
reservation_table = ttk.Treeview(

    reservation_frame,
    columns=("Customer", "Service", "Duration", "Status"),
    show="headings",
    height=4

)

reservation_table.heading("Customer", text="Customer")
reservation_table.heading("Service", text="Service")
reservation_table.heading("Duration", text="Duration")
reservation_table.heading("Status", text="Status")

reservation_table.column("Customer", width=220)
reservation_table.column("Service", width=220)
reservation_table.column("Duration", width=100)
reservation_table.column("Status", width=120)

reservation_table.grid(
    row=2,
    column=0,
    columnspan=6,
    padx=10,
    pady=10
)

# MAIN

if __name__ == "__main__":

    root.mainloop()