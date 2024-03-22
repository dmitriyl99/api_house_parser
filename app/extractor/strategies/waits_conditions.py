class element_has_unsecured_phone():
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if '*' in element.text:
            return False
        return element
