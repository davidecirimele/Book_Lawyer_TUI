import sys

from menu import Menu, Description, Entry
from appointments.domain import LawFirm, Appointment, Customer, Title, Subject, Date
from typing import Any, Tuple, Callable
from valid8 import validate, ValidationError
import getpass
import requests


class App:
    __menu = None
    api_server = 'http://localhost:8000/api/v1'
    username = None
    key = None

    def __init__(self):
        self.__menu = Menu.Builder(Description('Book a Lawyer')) \
            .with_entry(Entry.create('1', 'Login', on_selected=lambda: self.__login())) \
            .with_entry(Entry.create('2', 'Show all the appointments', on_selected=lambda: self.__show_appointments())) \
            .with_entry(Entry.create('3', 'Show an appointment',
                                     on_selected=lambda: self.__show_single_appointment())) \
            .with_entry(Entry.create('4', 'Book the Lawyer', on_selected=lambda: self.__book_the_lawyer())) \
            .with_entry(Entry.create('5', 'Manage appointment', on_selected=lambda: self.__delete_appointment())) \
            .with_entry(Entry.create('6', 'Log out', on_selected=lambda: self.__logout())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye bye!'), is_exit=True)) \
            .build()
        self.__dealer = LawFirm()

    # Press ⌃R to execute it or replace it with your code.
    # Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

    def __login(self):
        username = input("Username: ")
        password = getpass.getpass('Password: ')

        res = requests.post(url=f'{self.api_server}/auth/login/', data={'username': username, 'password': password})
        if res.status_code != 200:
            return None
        self.username = username
        json = res.json()
        print(f"Successfull logged in, json")
        self.key = json['key']
        return self.key

    def __logout(self):
        res = requests.post(url=f'{self.api_server}/auth/logout/', headers={'Authorization': f'Token {self.key}'})
        if res.status_code == 200:
            print("Logged out")
        else:
            print("Logout failed")
        print()

    def __fetch_appointments(self):
        if self.username == "Lawyer":
            res = requests.get(url=f'{self.api_server}/appointments/lawyer',
                               headers={'Authorization': f'Token {self.key}'})
        else:
            res = requests.get(url=f'{self.api_server}/appointments/customer',
                               headers={'Authorization': f'Token {self.key}'})
        if res.status_code != 200:
            return None
        return res.json()

    def __fetch_single_appointment(self, appointment_id):
        if self.username == "Lawyer":
            res = requests.get(url=f'{self.api_server}/appointments/lawyer/{appointment_id}',
                               headers={'Authorization': f'Token {self.key}'})
        else:
            res = requests.get(url=f'{self.api_server}/appointments/customer/{appointment_id}',
                               headers={'Authorization': f'Token {self.key}'})
        if res.status_code != 200:
            return None

        return res.json()

    def __show_appointments(self):
        appointments = self.__fetch_appointments()
        for app in appointments:
            print(app)

    def __show_single_appointment(self):
        appointment_id = input("Insert appointment ID: ")
        print(self.__fetch_single_appointment(appointment_id))

    def __add_appointment(self):
        if self.username == "Lawyer":
            res = requests.post(url=f'{self.api_server}/appointments/lawyer',
                                headers={'Authorization': f'Token {self.key}'},
                                data=('...'))
        else:
            res = requests.post(url=f'{self.api_server}/appointments/customer',
                                headers={'Authorization': f'Token {self.key}'},
                                data=('...'))
        return res.json()

    def __book_the_lawyer(self):
        appointment = self.__read_appointment()
        print(self.__add_appointment(appointment))


    def __delete_appointment(self):
        pass

    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)

    def __read_appointment(self) -> Tuple[Customer, Title, Subject, Date]:
        json = requests.get(url=f"{self.api_server}/auth/user/",headers={'Authorization': f'Token {self.key}'}).json()
        customer = json['pk']
        print(customer)
        title = self.__read('Title', Title)
        subject = self.__read('Subject', Subject)
        date = self.__read('Date', Date)
        return customer, title, subject, date

    def __run(self) -> None:
        self.__menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except Exception as e:
            print('Error!', file=sys.stderr)
            print(e)


def main(name: str):
    if name == '__main__':
        App().run()


main(__name__)
