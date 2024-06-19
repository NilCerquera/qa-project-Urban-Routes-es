import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import data

driver = webdriver.Chrome()  # Google Chrome
driver.maximize_window()  # Modo de pantalla completa


# no modificar ya que corresponde a la recuperación del codigo SMS al celular


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
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código"
                            " en tu aplicación.")
        return code


# Creamos un wait para realizar las pruebas correspondientes

# Ingresamos los localizadores de la App


def wait_load_page(from_field):
    WebDriverWait(driver, 3).until(expected_conditions.visibility_of_element_located(from_field))


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    button_order = (By.CLASS_NAME, "button.button.round")
    select_comfort = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")
    comfort_container = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']/..")
    button_phone_number = (By.CSS_SELECTOR, "div.np-button")
    input_number = (By.ID, "phone")
    select_number = (By.CLASS_NAME, "button.button.full")
    code_phone = (By.ID, "code")
    submit_code = (By.XPATH, ".//div[@class='modal']//button[text()='Confirmar']")
    button_payment = (By.CSS_SELECTOR, ".pp-button")
    add_credit_Card = (By.CSS_SELECTOR, ".pp-row.disabled")
    number_credit_card = (By.ID, "number")
    code_credit_card = (By.XPATH, ".//div[@class='card-code-input']/input[@id='code']")
    click_payment = (By.XPATH, ".//div[@class='pp-buttons']//button[text()='Agregar']")
    window_payment_closed = (By.CSS_SELECTOR, ".payment-picker.open .modal .section.active .close-button.section-close")
    driver_comment = (By.ID, "comment")
    blankets_and_handkerchiefs = (By.CSS_SELECTOR, '.reqs-body .r-type-switch:nth-of-type(1) .slider')
    switch_checkbox_blankets_and_handkerchiefs = (By.CSS_SELECTOR, 'input.switch-input')
    ice_cream_value = (By.CSS_SELECTOR, '.r-group-items .r-type-counter:nth-of-type(1) .counter-value')
    order_taxi_button = (By.CSS_SELECTOR, '.smart-button-main')
    order_header_title = (By.CSS_SELECTOR, '.order-header-title')

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

    def set_route(self, adrress_from, to):
        self.set_from(adrress_from)
        self.set_to(to)

    # Agregamos una espera implicita para el cargue de la página
    def wait_load_page(self):
        self.driver.implicitly_wait(3)

    # Agregamos una espera implicita para la espera del taxi y detalles

    def wait_message(self):
        self.driver.implicitly_wait(60)

    # Ingresamos una acción de seleccionar el taxi

    def click_order_taxi(self):
        self.driver.find_element(*self.button_order).click()

    # Ingresamos una acción para seleccion la opción comfort
    def box_comfort(self):
        self.driver.find_element(*self.select_comfort).click()

    # Ingresamos una acción para comprobar si nos devuelve la opción "Comfort"
    def is_comfort_selected(self):
        container = self.driver.find_element(*self.comfort_container)
        return "active" in container.get_attribute('class')

    # Damos Click para agregar el telefono
    def click_phone(self):
        self.driver.find_element(*self.button_phone_number).click()

    # Añadimos el número de telefono
    def add_number(self):
        self.driver.find_element(*self.input_number).send_keys(data.phone_number)

    # Comprobamos si el número guardado corresponde
    def get_number_phone(self):
        return self.driver.find_element(*self.input_number).get_property('value')  # Seleccionamos la opción continuar

    def select_continue(self):
        self.driver.find_element(*self.select_number).click()

    # Traemos el codigo SMS para el telefono y poder guardar el número telefonico
    def send_code(self, code):
        self.driver.find_element(*self.code_phone).send_keys(code)

    # Hacemos click en el botón para guardar el número de telefono
    def ok_code(self):
        self.driver.find_element(*self.submit_code).click()

    # Hacemos click en el botón agregar metodo de pago
    def click_payment_button(self):
        self.driver.find_element(*self.button_payment).click()

    # Seleccionamos la opción de nueva tarjeta
    def click_new_card(self):
        self.driver.find_element(*self.add_credit_Card).click()

    # Agregamos el número de tarjeta
    def add_number_card(self):
        self.driver.find_element(*self.number_credit_card).send_keys(data.card_number)
        self.driver.find_element(*self.number_credit_card).send_keys(Keys.TAB)

    # Comprobamos si se agrega el número de tarjeta
    def get_number_card(self):
        return self.driver.find_element(*self.number_credit_card).get_property('value')

    # Agregamos el codigo de seguridad de la tarjeta
    def add_code_card(self):
        self.driver.find_element(*self.code_credit_card).send_keys(data.card_code)
        self.driver.find_element(*self.code_credit_card).send_keys(Keys.TAB)

    # Comprobamos si se agrega el codigo de la tarjeta

    def get_code_credit_card(self):
        return self.driver.find_element(*self.code_credit_card).get_property('value')

    # Realizamos un click para agregar el metodo de pago
    def click_add_payment(self):
        self.driver.find_element(*self.click_payment).click()

    # Hacemos click para cerrar la pagina
    def click_window_closed_payment(self):
        self.driver.find_element(*self.window_payment_closed).click()

    # Agregamos un comentario al conductor
    def add_comment_driver(self):
        self.driver.find_element(*self.driver_comment).send_keys(data.message_for_driver)

    # Comprobamos si sel comentario del conductor es correcto a lo mencionado.
    def get_comment_driver(self):
        return self.driver.find_element(*self.driver_comment).get_property('value')

    # Seleccionamos la opcion manta y pañuelos

    def activate_slider_blankets_and_handkerchiefs(self):
        self.driver.find_element(*self.blankets_and_handkerchiefs).click()

    # Comprobamos si el selector se activa para seleccionar manta y pañuelos

    def is_switch_checked_blankets_and_handkerchiefs(self):
        checkbox = self.driver.find_element(*self.switch_checkbox_blankets_and_handkerchiefs)
        return checkbox.is_selected()

    # Agregamos helado al pedido
    def add_icecream_amount(self, new_value):
        counter_elements = self.driver.find_element(*self.ice_cream_value)
        self.driver.execute_script("arguments[0].textContent = arguments[1];", counter_elements, new_value)

    # Comprobamos si agregó dos helados

    def get_icecream_counter(self):
        return self.driver.find_element(*self.ice_cream_value).text

    # Hacemos click al pedido y esperamos para ver los detalles del pedido
    def click_order_taxi_button(self):
        self.driver.find_element(*self.order_taxi_button).click()

    # Comprobamos el mensaje de la página.

    def get_message(self):
        return self.driver.find_element(*self.order_header_title).text


# Aqui iniciamos las pruebas automatizadas
class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para
        # recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    # En esta prueba agregamos la direccion Desde y Hasta
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)  # todas las pruebas deben contener
        address_from = data.address_from
        address_to = data.address_to
        routes_page.wait_load_page()
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    # En esta prueba, seleccionamos la opción Comfort
    def test_select_comfort(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_load_page()
        routes_page.click_order_taxi()
        routes_page.box_comfort()
        routes_page.wait_load_page()
        assert routes_page.is_comfort_selected()

    # En esta prueba añadimos el telefono y codigo SMS enviado al usuario
    def test_add_phone(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_phone()
        routes_page.add_number()
        routes_page.wait_load_page()
        routes_page.select_continue()
        routes_page = UrbanRoutesPage(self.driver)
        code = retrieve_phone_code(driver=self.driver)
        routes_page.wait_load_page()
        routes_page.send_code(code)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_load_page()
        routes_page.ok_code()
        phone_number = data.phone_number
        assert routes_page.get_number_phone() == phone_number

    # En esta prueba agregamos la tarjeta de credito
    def test_credit_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_load_page()
        routes_page.click_payment_button()
        routes_page.wait_load_page()
        routes_page.click_new_card()
        routes_page.wait_load_page()
        routes_page.add_number_card()
        routes_page.wait_load_page()
        routes_page.add_code_card()
        routes_page.wait_load_page()
        routes_page.click_add_payment()
        routes_page.wait_load_page()
        routes_page.click_window_closed_payment()
        routes_page.wait_load_page()
        number_credit_card = data.card_number
        code_credit_card = data.card_code
        assert routes_page.get_number_card() == number_credit_card
        assert routes_page.get_code_credit_card() == code_credit_card

    # En esta prueba agregamos el mensaje al conductor.
    def test_comment_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_load_page()
        routes_page.add_comment_driver()
        routes_page.wait_load_page()
        comment_driver = data.message_for_driver
        assert routes_page.get_comment_driver() == comment_driver

    # En esta prueba seleccionamos Manta y pañuelos

    def test_slider_blankets_and_handkerchiefs(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.activate_slider_blankets_and_handkerchiefs()
        routes_page.wait_load_page()
        assert routes_page.is_switch_checked_blankets_and_handkerchiefs()

    # En esta prueba confirmamos 2 helados y comprobamos que se hayan agregado correctamente
    def test_click_two_ice_cream_value(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_load_page()
        counter_elements = '2'
        routes_page.add_icecream_amount(counter_elements)
        ice_cream_value = routes_page.get_icecream_counter()
        assert ice_cream_value == counter_elements

    # En esta prueba realizamos el pedido y comprobamos el mensaje final de la página.
    def test_order_taxi_button(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_order_taxi_button()
        routes_page.wait_message()
        time.sleep(60)
        final_message = routes_page.get_message()
        assert "El conductor llegará" in final_message

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
