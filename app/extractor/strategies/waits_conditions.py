class element_has_unsecured_phone():
    def __init__(self, parent_element, locator):
        self.locator = locator
        self.parent_element = parent_element

    def __call__(self, driver):
        element = self.parent_element.find_element(*self.locator)
        if '*' in element.text or element.text == 'Загрузка':
            return False
        return element
