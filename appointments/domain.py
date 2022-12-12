import re
from dataclasses import dataclass, InitVar, field
import datetime
from typing import Any, List
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
        validate('value', self.value, min_value=datetime.datetime.now())

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
    __appointments: List[Appointment] = field(default_factory=list, init=False)

    def clear(self):
        self.__appointments.clear()

    def appointments(self) -> int:
        return len(self.__appointments)

    def appointment(self, index: int):
        validate('index', index, min_value=0, max_value=self.appointments() - 1)

        return self.__appointments[index]

    def add_appointment(self, appointment: Appointment) -> None:
        self.__appointments.append(appointment)

    def remove_appointment(self, index: int) -> None:
        validate('index', index, min_value=0, max_value=self.appointments() - 1)

        del self.__appointments[index]

    def sort_by_date(self) -> None:
        self.__appointments.sort(key=lambda x: x.date, reverse=True)
