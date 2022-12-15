import datetime
import sys

import requests

from menu import Menu, Description, Entry
from appointments.domain import LawFirm, Appointment, Customer, Title, Subject, Date
from typing import Any, Tuple, Callable
from valid8 import validate, ValidationError
import getpass

LAWYER_USERNAME = "Lawyer"


class App:
    __menu = None
    api_server = 'http://localhost:8000/api/v1'
    username = None
    key = None

    def __init__(self):
        self.__menu = Menu.Builder(Description('Book a Lawyer')) \
            .with_entry(Entry.create('1', 'Login', on_selected=lambda: self.__login())) \
            .with_entry(Entry.create('2', 'Register', on_selected=lambda: self.__register())) \
            .with_entry(Entry.create('3', 'Show all the appointments',
                                     on_selected=lambda: self.__show_appointments())) \
            .with_entry(Entry.create('4', 'Show an appointment',
                                     on_selected=lambda: self.__show_single_appointment())) \
            .with_entry(Entry.create('5', 'Book the Lawyer', on_selected=lambda: self.__book_the_lawyer())) \
            .with_entry(Entry.create('6', 'Manage appointment', on_selected=lambda: self.__manage_appointment())) \
            .with_entry(Entry.create('7', 'Log out', on_selected=lambda: self.__logout())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye bye!'), is_exit=True)) \
            .build()
        self.__law_firm = LawFirm()

    def __login(self):
        if self.username is not None:
            print("Already logged in")
            return
        username = input("Username: ")
        password = getpass.getpass('Password: ')

        res = requests.post(url=f'{self.api_server}/auth/login/', data={'username': username, 'password': password})
        if res.status_code != 200:
            print("Failed to log in, please try again")
            return None
        self.username = username
        json = res.json()
        print("Successful logged in, Welcome")
        self.key = json['key']
        return self.key

    def __register(self):
        if self.username is not None:
            print("Already logged in")
            return

        username = input("Please enter an Username: ")
        email = input("Please enter a valid email: ")
        password1 = getpass.getpass('Please enter a Password: ')
        password2 = getpass.getpass('Please, confirm Password: ')

        res = requests.post(url=f'{self.api_server}/auth/registration/', data={'username': username, 'email': email,
                                                                               'password1': password1,
                                                                               'password2': password2})
        if res.status_code != 200:
            return None

        return res.json()

    def __logout(self):
        if self.username is None:
            print("Already not logged in")
            return
        res = requests.post(url=f'{self.api_server}/auth/logout/', headers={'Authorization': f'Token {self.key}'})
        if res.status_code == 200:
            self.username = None
            print("Logged out")
        else:
            print("Logout failed")
        print()

    def __show_appointments(self):
        if self.username is None:
            print("You must be logged in")
            return
        appointments = list(self.__law_firm.fetch_appointments(self.key, self.username))
        appointments.sort(key=lambda x: x['date'])
        self.__print_appointments(appointments)

    def __show_single_appointment(self):
        if self.username is None:
            print("You must be logged in")
            return
        appointment_id = input("Insert appointment ID: ")
        self.__print_appointment(self.__law_firm.fetch_single_appointment(appointment_id, self.key, self.username))

    def __book_the_lawyer(self):
        if self.username is None:
            print("You must be logged in")
            return
        appointment = Appointment(*self.__read_appointment())
        self.__print_appointment(self.__law_firm.add_appointment(appointment, self.key, self.username))

    def __change_the_appointment(self):
        appointment_to_update = input("Insert appointment ID you want to modify: ")
        appointment = Appointment(*self.__read_appointment())
        self.__print_appointment(
            self.__law_firm.update_appointment(appointment, appointment_to_update, self.key, self.username))

    def __manage_appointment(self):
        if self.username is None:
            print("You must be logged in")
            return
        selection = input("1. To modify an appointment,\n"
                          "2. To delete an appointment.\n"
                          "0. Back. \n"
                          "What do you want to do? ")

        if selection == '1':
            self.__change_the_appointment()
        elif selection == '2':
            self.__law_firm.delete_appointment(self.key, self.username)
        elif selection == '0':
            pass

    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                if line.isdigit():
                    res = builder(int(line.strip()))
                else:
                    res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)

    def __read_appointment(self) -> Tuple[Customer, Title, Subject, Date]:
        if self.username == LAWYER_USERNAME:
            customer = self.__read('Customer', Customer)
        else:
            json = requests.get(url=f"{self.api_server}/auth/user/",
                                headers={'Authorization': f'Token {self.key}'}).json()
            customer = Customer(json['pk'])
        title = self.__read('Title', Title)
        subject = self.__read('Subject', Subject)
        year = input("Please insert the year of the appointment: ")
        month = input("Please insert the month of the appointment: ")
        day = input("Please insert the day of the appointment: ")
        hour = input("Please insert the hour of the appointment: ")
        minutes = input("Please insert the minutes of the appointment: ")
        date = Date(datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes)))
        return customer, title, subject, date

    def __print_appointments(self, appointments) -> None:
        print_sep = lambda: print('-' * 140)
        print_sep()
        fmt = '%-3s %-10s %-20s %-80s %10s'
        print(fmt % ('ID', 'CUSTOMER', 'TITLE', 'SUBJECT', 'DATE'))
        print_sep()
        for appointment in appointments:
            print(fmt % (appointment['id'], appointment['customer'], appointment['title'], appointment['subject'],
                         appointment['date']))
        print_sep()

    def __print_appointment(self, appointment) -> None:
        print_sep = lambda: print('-' * 140)
        print_sep()
        fmt = '%-3s %-10s %-20s %-80s %10s'
        print(fmt % ('ID', 'CUSTOMER', 'TITLE', 'SUBJECT', 'DATE'))
        print_sep()
        print(fmt % (
            appointment['id'], appointment['customer'], appointment['title'], appointment['subject'],
            appointment['date']))
        print_sep()

    def __run(self) -> None:
        self.__menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except:
            print('Error!', file=sys.stderr)


def main(name: str):
    if name == '__main__':
        App().run()


main(__name__)
