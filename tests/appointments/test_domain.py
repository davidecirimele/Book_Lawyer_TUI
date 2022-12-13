import datetime

import pytest
from valid8 import ValidationError
from appointments.domain import Customer, Title, Subject, Date, Appointment, LawFirm


def test_author_str():
    assert str(Customer(1)) == '1'


def test_title_format():
    with pytest.raises(ValidationError):
        Title('A'*31)


def test_subject_format():
    with pytest.raises(ValidationError):
        Title('A'*201)


@pytest.fixture
def appointments():
    return [
        Appointment(Customer(1), Title("Divorzio"), Subject("Voglio divorzio"), Date(datetime.datetime(2030, 1, 1))),
        Appointment(Customer(2), Title("Denuncia"), Subject("Voglio denunciare"), Date(datetime.datetime(2030, 1, 2))),
    ]


def test_clear_len_add_appointments(appointments):
    law_firm = LawFirm()
    size = 0
    for appointment in appointments:
        law_firm.add_appointment(appointment)
        size += 1
        assert law_firm.appointments() == size
        assert law_firm.appointment((size - 1)) == appointment
    law_firm.clear()
    assert law_firm.appointments() == 0


def test_remove_appointment(appointments):
    law_firm = LawFirm()
    for appointment in appointments:
        law_firm.add_appointment(appointment)

    law_firm.remove_appointment(0)
    assert law_firm.appointment(0) == appointments[1]

    with pytest.raises(ValidationError):
        law_firm.remove_appointment(-1)

    with pytest.raises(ValidationError):
        law_firm.remove_appointment(law_firm.appointments())

    while law_firm.appointments():
        law_firm.remove_appointment(0)
    assert law_firm.appointments() == 0
