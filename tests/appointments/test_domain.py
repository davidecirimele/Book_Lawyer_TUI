import datetime

import pytest
from unittest import mock
from unittest.mock import patch
from valid8 import ValidationError
from appointments.domain import Customer, Title, Subject, Date, Appointment, LawFirm
from app import App


def test_author_str():
    assert str(Customer(1)) == '1'


def test_title_format():
    with pytest.raises(ValidationError):
        Title('A' * 31)


def test_title_str():
    assert str(Title('A')) == 'A'


def test_subject_format():
    with pytest.raises(ValidationError):
        Title('A' * 201)


def test_subject_str():
    assert str(Subject('A')) == 'A'


def test_date_str():
    assert str(Date(datetime.datetime(1, 1, 1, 1, 1))) == '0001-01-01 01:01:00'


def test_law_firm_fetch_appointments():
    law_firm = LawFirm()
    response = law_firm.fetch_appointments("Q", "A")
    assert response is None


def test_law_firm_fetch_single_appointment():
    law_firm = LawFirm()
    response = law_firm.fetch_single_appointment("A", "Q", "A")
    assert response is None


def test_law_firm_add_appointment():
    law_firm = LawFirm()
    response = law_firm.add_appointment(
        Appointment(Customer(1), Title("A"), Subject("A"), Date(datetime.datetime(1, 1, 1, 1, 1))), "Q", "A")
    assert response is None


@patch('builtins.input', side_effect=['2'])
@patch('builtins.print')
def test_law_firm_delete_appointment(mocked_input, mocked_print):
    law_firm = LawFirm()
    law_firm.delete_appointment("A", "B")
    mocked_print.assert_called()


def test_law_firm_update_appointment():
    law_firm = LawFirm()
    response = law_firm.update_appointment(
        Appointment(Customer(1), Title("A"), Subject("A"), Date(datetime.datetime(1, 1, 1, 1, 1))), "Q", "A", "U")
    assert response is None

