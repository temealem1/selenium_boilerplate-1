from selenium.webdriver.common.by import By

ADD_ACTION_BUTTON = {
    'by': By.XPATH,
    'value': '//button[text()="+ Add"]'
}

EMPTY_STATE_ADD_ACTION_BUTTON = {
    'by': By.CSS_SELECTOR,
    'value': '.actions-search__empty-content button'
}

EMPTY_STATE_HELP_TEXT = {
    'by': By.CSS_SELECTOR,
    'value': '.actions-search__empty-content h5'
}


def action_count_by_description(description):
    return {
        'by': By.XPATH,
        'value': f'//figcaption[contains(string(), "{description}")]//preceding-sibling::figure'
    }


def action_end_by_position(position):
    return {
        'by': By.XPATH,
        'value': f'//tr[contains(@class, "actions-row__info")][{position}]//td[contains(@class, "actions-row__date-col")][2]'
    }


def action_start_by_position(position):
    return {
        'by': By.XPATH,
        'value': f'//tr[contains(@class, "actions-row__info")][{position}]//td[contains(@class, "actions-row__date-col")][1]'
    }
