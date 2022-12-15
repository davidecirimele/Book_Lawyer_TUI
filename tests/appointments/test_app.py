import datetime

import pytest
from unittest import mock
from unittest.mock import patch
from valid8 import ValidationError
from appointments.domain import Customer, Title, Subject, Date, Appointment, LawFirm
from app import App, main


@patch('builtins.input', side_effect=['3'])
@patch('builtins.print')
def test_show_all_appointments(mocked_print, mocked_input):
    with patch.object(LawFirm, 'fetch_appointments') as mocked:
        app = App()
        app.username = "TEST"
        app.run()
        mocked.assert_called()


@patch('builtins.input', side_effect=['4', '3'])
@patch('builtins.print')
def test_show_single_appointment(mocked_print, mocked_input):
    with patch.object(LawFirm, 'fetch_single_appointment') as mocked:
        app = App()
        app.username = "TEST"
        app.run()
        mocked.assert_called()


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_exit(mocked_print, mocked_input):
    main('__main__')
    mocked_print.assert_called_with('Bye bye!')


@patch('builtins.input', side_effect=['1', 'test', 'test'])
@patch('builtins.print')
def test_login(mocked_print, mocked_input):
    App().run()
    mocked_input.assert_called_with("Username: ")


@patch('builtins.input', side_effect=['1'])
@patch('builtins.print')
def test_login_wrong(mocked_print, mocked_input):
    app = App()
    app.username = "Test"
    app.run()
    mocked_print.assert_any_call("Already logged in")


@patch('builtins.input', side_effect=['2', 'test', 'test@test.com', 'test', 'test'])
@patch('builtins.print')
def test_register(mocked_print, mocked_input):
    App().run()
    mocked_input.assert_called_with("Please enter a valid email: ")


@patch('builtins.input', side_effect=['2'])
@patch('builtins.print')
def test_register_wrong(mocked_print, mocked_input):
    app = App()
    app.username = "TEST"
    app.run()
    mocked_print.assert_any_call("Already logged in")


@patch('builtins.input', side_effect=['7'])
@patch('builtins.print')
def test_logout(mocked_print, mocked_input):
    app = App()
    app.username = "TEST"
    app.run()
    mocked_print.assert_any_call("Logout failed")


@patch('builtins.input', side_effect=['7'])
@patch('builtins.print')
def test_logout_wrong(mocked_print, mocked_input):
    App().run()
    mocked_print.assert_any_call("Already not logged in")


@patch('builtins.input', side_effect=['6', '0'])
@patch('builtins.print')
def test_manage_appointments_go_back(mocked_print, mocked_input):
    app = App()
    app.username = "TEST"
    app.run()
    mocked_input.assert_any_call("1. To modify an appointment,\n"
                                 "2. To delete an appointment.\n"
                                 "0. Back. \n"
                                 "What do you want to do? ")


@patch('builtins.input', side_effect=['5'])
@patch('builtins.print')
def test_book_the_lawyer_wrong(mocked_print, mocked_input):
    app = App()
    app.run()
    mocked_print.assert_any_call("You must be logged in")


@patch('builtins.input', side_effect=['6'])
@patch('builtins.print')
def test_manage_appointments_wrong(mocked_print, mocked_input):
    app = App()
    app.run()
    mocked_print.assert_any_call("You must be logged in")


@patch('builtins.input', side_effect=['6', '2'])
@patch('builtins.print')
def test_delete_appointment(mocked_print, mocked_input):
    app = App()
    app.username = "Lawyer"
    app.run()
    mocked_input.assert_any_call("1. To modify an appointment,\n"
                                 "2. To delete an appointment.\n"
                                 "0. Back. \n"
                                 "What do you want to do? ")


@patch('builtins.input', side_effect=['6', '2'])
@patch('builtins.print')
def test_delete_appointment_customer(mocked_print, mocked_input):
    app = App()
    app.username = "TEST"
    app.run()
    mocked_input.assert_any_call("1. To modify an appointment,\n"
                                 "2. To delete an appointment.\n"
                                 "0. Back. \n"
                                 "What do you want to do? ")


@patch('builtins.input', side_effect=['6', '1', 1, 'Title', 'Subject', '2030', '1', '1', '1', '1'])
@patch('builtins.print')
def test_change_the_appointment(mocked_print, mocked_input):
    app = App()
    app.username = "Lawyer"
    app.run()
    mocked_input.assert_any_call("Insert appointment ID you want to modify: ")
