import sys

from Menu import Menu, Description, Entry
from appointments.domain import Law_firm
import getpass
import requests

class Application:

    __menu = None
    api_server = 'http://localhost:8000/api/v1'
    username = None
    key = None

    def __init__(self):
        self.__menu = Menu.Builder(Description('Book a Lawyer Application from Command Line'),
        auto_select=lambda: print('Welcome to Book a Lawyer!')) \
        .with_entry(Entry.create('1', 'Login', on_selected=lambda: self.__login())) \
        .with_entry(Entry.create('2', 'Show all the appointments', on_selected=lambda: self.__show_appointments())) \
        .with_entry(Entry.create('3', 'Show an appointment given a key', on_selected=lambda: self.__show_specific_appointment())) \
        .with_entry(Entry.create('4', 'Book the Lawyer', on_selected=lambda: self.__book_the_lawyer())) \
        .with_entry(Entry.create('5', 'Delete appointment', on_selected=lambda: self.__delete_appointment())) \
        .with_entry(Entry.create('6', 'Log out', on_selected=lambda: self.__logout())) \
        .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye bye!'), is_exit=True))\
        .build()
        self.__dealer = Law_firm()
        self.__my_key = None



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
        print("Successfull logged in")
        self.key = json['key']
        return self.key

    def __logout(self):
        res = requests.post(url=f'{self.api_server}/auth/logout/', headers={'Authorization': f'Token {self.key}'})
        if res.status_code == 200:
            print("Logged out")
        else:
            print("Logout failed")
        print()

    def __fetch_appointments(self,key):
        if self.username == "Lawyer":
            res = requests.get(url=f'{self.api_server}/appointments/lawyer', headers={'Authorization': f'Token {self.key}'})
        else:
            res = requests.get(url=f'{self.api_server}/appointments/customer', headers={'Authorization': f'Token {self.key}'})
        if res.status_code != 200:
            return None
        return res.json()

    def __show_appointments(self):
        appointments = self.__fetch_appointments(self.key)
        for app in appointments:
            print(app)

    def __show_specific_appointment(self,appointments,key):
        pass

    def __book_the_lawyer(self):
        pass

    def __delete_appointment(self):
        pass


    def __run(self) -> None:
        self.__menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except:
            print('Error during execution!', file=sys.stderr)

def main(name: str):
    if name == '__main__':
        Application().run()

main(__name__)