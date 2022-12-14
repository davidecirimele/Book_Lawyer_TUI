import datetime

import pytest
from unittest import mock
from unittest.mock import patch
from valid8 import ValidationError
from appointments.domain import Customer, Title, Subject, Date, Appointment, LawFirm
from app import App, main


@patch('builtins.input', side_effect=['3'])
@patch('builtins.print')
def test_show_all_appointments(mock_print, mock_input):
    with patch.object(LawFirm, 'fetch_appointments') as mocked:
        app = App()
        app.username = "TEST"
        app.run()
        mocked.assert_called()


@patch('builtins.input', side_effect=['4', '3'])
@patch('builtins.print')
def test_show_single_appointment(mock_print, mock_input):
    with patch.object(LawFirm, 'fetch_single_appointment') as mocked:
        app = App()
        app.username = "TEST"
        app.run()
        mocked.assert_called()


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_for_more_coverage(mock_print, mock_input):
    main('__main__')
    mock_print.assert_called()

# Customer(1), Title('Title'), Subject('Subject'), Date(datetime.datetime(2030, 1, 1, 1, 1))


@patch('builtins.input', side_effect=['1', 'test', 'test'])
@patch('builtins.print')
def test_login(mock_print, mock_input):
    App().run()


@patch('builtins.input', side_effect=['1', 'test', 'test'])
@patch('builtins.print')
def test_login_wrong(mock_print, mock_input):
    app = App()
    app.username = "TEST"
    app.run()


@patch('builtins.input', side_effect=['2', 'test', 'test@test.com', 'test', 'test'])
@patch('builtins.print')
def test_register(mock_print, mock_input):
    App().run()


@patch('builtins.input', side_effect=['2', 'test', 'test@test.com', 'test', 'test'])
@patch('builtins.print')
def test_register_wrong(mock_print, mock_input):
    app = App()
    app.username = "TEST"
    app.run()



@patch('builtins.input', side_effect=['7'])
@patch('builtins.print')
def test_logout(mock_print, mock_input):
    app = App()
    app.username = "TEST"
    app.run()

