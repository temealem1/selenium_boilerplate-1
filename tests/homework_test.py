import logging
import pytest
import requests

from datetime import datetime
from random import choice
from selenium.webdriver.common.by import By
from time import sleep

from api import actions, authorization, current_user
from pages.actions_page.page_object import ActionsPage
from pages.action_modal.page_object import ActionModal
from pages.confirmation_modal.page_object import ConfirmationModal
from pages.home_page.page_object import HomePage
from pages.login_page.page_object import LoginPage
from utilities.validators import date_is_valid, time_is_valid
from utilities.wait import wait_for_element_to_be_visible


def delete_icon_by_action_summary(action_summary):
    return {
        'by': By.XPATH,
        'value': f'//p[text()="{action_summary}"]//ancestor::tr//i[@class="ion-trash-b"]'
    }


def new_action_summary(summary_text):
    return {
        'by': By.XPATH,
        'value': f'//td[contains(@class, "actions-row__summary-col")]//p[text()="{summary_text}"]'
    }


def get_random_number():
    return choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


def get_date():
    date = datetime.now()

    return f'{date.month}/{date.day}/{date.year}'


def get_timestamp():
    date = datetime.now()

    return f'{date.hour}:{date.minute}:{date.second}'


def test_action_counts_for_empty_state(driver):
    login_page = LoginPage(driver)
    login_page.login('selenium.course@fiscalnote.com', 'not_my_real_password')

    home_page = HomePage(driver)
    assert "Welcome" in home_page.welcome_message

    actions_page = ActionsPage(driver)
    actions_page.navigate()

    assert actions_page.total_actions_count == 0
    assert actions_page.actions_this_week_count == 0
    assert actions_page.actions_this_month_count == 0

    assert "No actions yet." in actions_page.empty_state_help_text
    assert "Create one to record meetings, calls, and other actions to share past and future activity with your team." in actions_page.empty_state_help_text

    assert actions_page.empty_state_add_action_button.is_displayed()


def test_user_sees_correct_default_state_for_action_modal(driver):
    pass


def test_user_can_open_actions_modal_with_empty_state_add_action_button_and_close_it_with_cancel_button(driver):
    login_page = LoginPage(driver)
    login_page.login('selenium.course@fiscalnote.com', 'not_my_real_password')

    home_page = HomePage(driver)
    assert "Welcome" in home_page.welcome_message

    actions_page = ActionsPage(driver)
    actions_page.navigate()
    actions_page.click_empty_state_add_action_button()

    action_modal = ActionModal(driver)

    assert action_modal.is_displayed

    assert action_modal.modal_header_text == "Add Action"

    assert date_is_valid(action_modal.start_date_value)

    assert time_is_valid(action_modal.start_time_value)

    assert date_is_valid(action_modal.end_date_value)

    assert time_is_valid(action_modal.end_time_value)

    assert action_modal.selected_action_type == "Meeting"

    assert action_modal.added_attendees == ['Selenium Course']

    assert action_modal.added_linked_items == []

    assert action_modal.added_labels == []

    assert action_modal.added_issues == []

    assert action_modal.current_summary_text == ''

    action_modal.click_cancel_button()

    confirmation_modal = ConfirmationModal(driver)
    confirmation_modal.click_cancel_button()

    assert action_modal.is_displayed

    action_modal.click_cancel_button()
    confirmation_modal.click_confirm_button()

    assert action_modal.is_not_displayed


def test_user_can_open_actions_modal_with_main_add_action_button_and_close_it_with_x_icon(driver):
    login_page = LoginPage(driver)
    login_page.login('selenium.course@fiscalnote.com', 'not_my_real_password')

    home_page = HomePage(driver)

    welcome_message = "Welcome, Selenium"
    logging.info(f'Verifying that the text "{welcome_message}" appears in the welcome message on the Home Page.')
    assert welcome_message in home_page.welcome_message

    actions_page = ActionsPage(driver)
    actions_page.navigate()
    actions_page.click_add_action_button()

    action_modal = ActionModal(driver)

    logging.info('Verifying Action Modal is visible.')
    assert action_modal.is_displayed

    action_modal.click_close_icon()

    confirmation_modal = ConfirmationModal(driver)
    confirmation_modal.click_cancel_button()

    logging.info('Verifying Action Modal is still visible.')
    assert action_modal.is_displayed

    action_modal.click_close_icon()
    confirmation_modal.click_confirm_button()

    logging.info('Verifying Action Modal is no longer visible.')
    assert action_modal.is_not_displayed


def test_user_can_create_a_new_action(driver):
    login_page = LoginPage(driver)
    login_page.login('', '')

    home_page = HomePage(driver)
    assert "Welcome" in home_page.welcome_message

    actions_page = ActionsPage(driver)
    actions_page.navigate()

    # actions_page.click_add_action_button()
    #
    # action_modal = ActionModal(driver)
    # action_modal.enter_start_date('8/14/2019')
    # action_modal.enter_start_time('6:00am')
    # action_modal.enter_end_date('8/14/2019')
    # action_modal.enter_end_time('5:00pm')
    # action_modal.set_action_type('Phone Call')
    # action_modal.add_linked_item('US HR 1478', 'US - HR 1478')
    # action_modal.add_labels(('agriculture', 'Farming', 'welfare'))
    # action_modal.add_issue('Agriculture')
    #
    # action_summary_text = f'{get_date()} {get_timestamp()} - This is my summary text.'
    # action_modal.add_summary(action_summary_text)
    #
    # action_modal.click_save_button()

    # expected_action_1_start = "Mar 27, 2020 2:08 PM"
    # logging.info(f'Verifying that the "Start" value for the action in position 1 equals "{expected_action_1_start}"')
    # assert actions_page.get_action_start_by_position(1) == expected_action_1_start
    #
    # expected_action_1_end = "Mar 27, 2020 3:08 PM"
    # logging.info(f'Verifying that the "End" value for the action in position 1 equals "{expected_action_1_end}"')
    # assert actions_page.get_action_end_by_position(1) == expected_action_1_end
    #
    # expected_action_2_start = "Mar 27, 2020 2:08 PM"
    # logging.info(f'Verifying that the "Start" value for the action in position 2 equals "{expected_action_2_start}"')
    # assert actions_page.get_action_start_by_position(2) == expected_action_2_start
    #
    # expected_action_2_end = "Mar 27, 2020 3:08 PM"
    # logging.info(f'Verifying that the "End" value for the action in position 2 equals "{expected_action_2_end}"')
    # assert actions_page.get_action_end_by_position(2) == expected_action_2_end
    #
    # expected_action_3_start = "Mar 4, 2020 2:08 PM"
    # logging.info(f'Verifying that the "Start" value for the action in position 3 equals "{expected_action_3_start}"')
    # assert actions_page.get_action_start_by_position(3) == expected_action_3_start
    #
    # expected_action_3_end = "Mar 5, 2020 3:08 PM"
    # logging.info(f'Verifying that the "End" value for the action in position 3 equals "{expected_action_3_end}"')
    # assert actions_page.get_action_end_by_position(3) == expected_action_3_end

    # expected_creator = 'Tem Automation'
    # logging.info(f'Verifying that the "Creator" value for the action in position 1 equals "{expected_creator}"')
    # assert actions_page.get_action_creator_by_position(1) == expected_creator
    #
    # expected_attendees = ['Herm Automation', 'Selenium Course', 'Tem Automation']
    # logging.info(f'Verifying that the "Attendees" value for the action in position 1 equals "{expected_attendees}"')
    # assert actions_page.get_action_attendees_by_position(1) == expected_attendees

    expected_issues = ['Agriculture', 'Farming', 'Welfare']
    logging.info(f'Verifying that the "Issues" value for the action in position 1 equals "{expected_issues}"')
    assert actions_page.get_action_issues_by_position(1) == expected_issues

    expected_summary = 'Edit summary and find the position'
    logging.info(f'Verifying that the "Summary" value for the action in position 1 equals "{expected_summary}"')
    assert actions_page.get_action_summary_by_position(1) == expected_summary


@pytest.mark.api
def test_api():
    auth_header = authorization.get_authorization_header('selenium.course@fiscalnote.com', '')
    user = current_user.get_current_user(auth_header)

    # action = actions.create_action(auth_header, action_type='Roundtable', summary='This is a custom summary.')

    for number in range(1, 11):
        actions.create_action(auth_header, summary=f'Action #{number}')

    actions.delete_all_actions(auth_header)


@pytest.mark.homework_solution
def test_user_can_delete_action(driver):
    auth_header = authorization.get_authorization_header('selenium.course@fiscalnote.com', 'April291!')
    actions.delete_all_actions(auth_header)
    action = actions.create_action(auth_header, summary='This action needs to be deleted.')

    login_page = LoginPage(driver)
    login_page.login('selenium.course@fiscalnote.com', '')

    home_page = HomePage(driver)
    assert "Welcome" in home_page.welcome_message

    actions_page = ActionsPage(driver)
    actions_page.navigate()
    actions_page.click_delete_action_icon_by_position(1)

    confirmation_modal = ConfirmationModal(driver)

    logging.info('Verifying that the "Delete Action" modal is visible.')
    assert confirmation_modal.is_displayed
    assert confirmation_modal.modal_title == 'Delete Action'

    confirmation_modal.click_cancel_button()

    logging.info('Verifying that the "Delete Action" modal is not visible.')
    assert confirmation_modal.is_not_displayed

    logging.info('Verifying that the action in position 1 has a summary of "This action needs to be deleted."')
    assert actions_page.get_action_summary_by_position(1) == 'This action needs to be deleted.'

    actions_page.click_delete_action_icon_by_position(1)
    confirmation_modal.click_ok_button()

    # Todo: make sure no actions are visible
    assert actions_page.total_actions_count == 0
