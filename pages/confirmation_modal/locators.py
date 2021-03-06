from selenium.webdriver.common.by import By

CANCEL_BUTTON = {
    'by': By.XPATH,
    'value': "//div[@class='modal-footer']//button[@class='btn btn-default'][contains(text(),'Cancel')]"
}

CONFIRM_BUTTON = {
    'by': By.CSS_SELECTOR,
    'value': '.modal-dialog--inner .modal-footer .btn-success'
}

MODAL_CONTAINER = {
    'by': By.CLASS_NAME,
    'value': 'modal-dialog--inner'
}

MODAL_TITLE = {
    'by': By.CSS_SELECTOR,
    'value': '.modal-header .modal-title'
}

OK_BUTTON = {
    'by': By.CSS_SELECTOR,
    'value': '.modal-footer .btn-success'
}
