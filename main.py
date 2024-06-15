from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import data
import main

driver = webdriver.Chrome() # Google Chrome

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code



class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    button_order = (By.CLASS_NAME, "button.button.round")
    select_comfort = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")
    button_phone_number = (By.CSS_SELECTOR, "div.np-button" )
    input_number = (By.ID, "phone")
    select_number = (By.CLASS_NAME, "button.button.full")
    code_phone = (By.ID, "code")


    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self,adrress_from,to):
        self.set_from(adrress_from)
        self.set_to(to)

    def click_order_taxi(self):
        self.driver.find_element(*self.button_order).click()

    def box_comfort(self):
        self.driver.find_element(*self.select_comfort).click()

    def click_phone(self):
        self.driver.find_element(*self.button_phone_number).click()

    def add_number(self):
        self.driver.find_element(*self.input_number).send_keys(data.phone_number)

    def select_continue(self):
        self.driver.find_element(*self.select_number).click()

    def send_code(self,code):
        self.driver.find_element(*self.code_phone).send_keys(code)

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver) # todas las pruebas deben contener
        address_from = data.address_from
        address_to = data.address_to
        time.sleep(3)
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort(self):
        routes_page = UrbanRoutesPage(self.driver)
        time.sleep(2)
        routes_page.click_order_taxi()
        routes_page.box_comfort()

    def test_add_phone(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_phone()
        routes_page.add_number()
        time.sleep(2)
        routes_page.select_continue()

    def test_code(self):
        routes_page = UrbanRoutesPage(self.driver)
        code = retrieve_phone_code(driver=self.driver)
        time.sleep(2)
        routes_page.send_code(code)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()