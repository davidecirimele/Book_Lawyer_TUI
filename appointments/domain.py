import re
from dataclasses import dataclass, InitVar, field
import datetime
from typing import Any, List

import requests
from typeguard import typechecked
from valid8 import validate

from validation.dataclasses import validate_dataclass
from validation.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Customer:
    value: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value)

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Title:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, max_len=30, min_len=1, custom=pattern(r'^[\w\s.:;]*$'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(order=True, frozen=True)
class Subject:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, max_len=200, min_len=1, custom=pattern(r'^[\w\s.:;]*$'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Date:
    value: datetime.datetime

    def __post_init__(self):
        validate_dataclass(self)

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Appointment:
    customer: Customer
    title: Title
    subject: Subject
    date: Date

    def __post_init__(self):
        validate_dataclass(self)


@typechecked
@dataclass(frozen=True)
class LawFirm:
    api_server = 'http://localhost:8000/api/v1'
    LAWYER_USERNAME = "Lawyer"

    def fetch_appointments(self,key,username):
        if username == "Lawyer":
            res = requests.get(url=f'{self.api_server}/appointments/lawyer/',
                               headers={'Authorization': f'Token {key}'})
        else:
            res = requests.get(url=f'{self.api_server}/appointments/customer/',
                               headers={'Authorization': f'Token {key}'})
        if res.status_code != 200:
            return None

        return res.json()

    def fetch_single_appointment(self, appointment_id,key,username):
        if username == "Lawyer":
            res = requests.get(url=f'{self.api_server}/appointments/lawyer/{appointment_id}',
                               headers={'Authorization': f'Token {key}'})
        else:
            res = requests.get(url=f'{self.api_server}/appointments/customer/{appointment_id}',
                               headers={'Authorization': f'Token {key}'})
        if res.status_code != 200:
            return None

        return res.json()

    def add_appointment(self, appointment: Appointment,key,username):
        if username is None:
            print("You must be logged in")
            return
        if username is self.LAWYER_USERNAME:
            url = f'{self.api_server}/appointments/lawyer/'
        else:
            url = f'{self.api_server}/appointments/customer/'

        res = requests.post(url=url,
                            headers={'Authorization': f'Token {key}'},
                            data={"customer": appointment.customer.value, "title": appointment.title.value,
                                  "subject": appointment.subject.value, "date": appointment.date.value})

        return res.json()

    def delete_appointment(self,key,username):
        appointment_to_delete = input("Insert appointment ID you want to delete: ")

        if username is self.LAWYER_USERNAME:
            url = f'{self.api_server}/appointments/lawyer/{appointment_to_delete}/'
        else:
            url = f'{self.api_server}/appointments/customer/{appointment_to_delete}/'

        res = requests.delete(url=url, headers={'Authorization': f'Token {key}'})

        if res.status_code == 204:
            print("Appointment successfully deleted")
        else:
            print("Appointment not deleted")

    def update_appointment(self,appointment : Appointment,appointment_to_update,key,username):

        if username is self.LAWYER_USERNAME:
            url = f'{self.api_server}/appointments/lawyer/{appointment_to_update}/'
        else:
            url = f'{self.api_server}/appointments/customer/{appointment_to_update}/'

        res = requests.put(url=url,
                            headers={'Authorization': f'Token {key}'},
                            data={"customer": appointment.customer.value, "title": appointment.title.value,
                                  "subject": appointment.subject.value, "date": appointment.date.value})

        return res.json()
