import time

import data
from selenium import webdriver
from UrbanRoutesPage import UrbanRoutesPage
import helpers
from helpers import retrieve_phone_code


driver = webdriver.Chrome()  # Google Chrome
driver.maximize_window()  # Modo de pantalla completa


# Aqui iniciamos las pruebas automatizadas
class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
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
        helpers.wait_load_page(self)
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    # En esta prueba, seleccionamos la opción Comfort
    def test_select_comfort(self):
        routes_page = UrbanRoutesPage(self.driver)
        helpers.wait_load_page(self)
        routes_page.click_order_taxi()
        routes_page.box_comfort()
        helpers.wait_load_page(self)
        assert routes_page.is_comfort_selected()

    # En esta prueba añadimos el telefono y codigo SMS enviado al usuario
    def test_add_phone(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_phone()
        routes_page.add_number()
        helpers.wait_load_page(self)
        routes_page.select_continue()
        routes_page = UrbanRoutesPage(self.driver)
        code = retrieve_phone_code(driver=self.driver)
        helpers.wait_load_page(self)
        routes_page.send_code(code)
        routes_page = UrbanRoutesPage(self.driver)
        helpers.wait_load_page(self)
        routes_page.ok_code()
        phone_number = data.phone_number
        assert routes_page.get_number_phone() == phone_number

    # En esta prueba agregamos la tarjeta de credito
    def test_credit_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        helpers.wait_load_page(self)
        routes_page.click_payment_button()
        helpers.wait_load_page(self)
        routes_page.click_new_card()
        helpers.wait_load_page(self)
        routes_page.add_number_card()
        helpers.wait_load_page(self)
        routes_page.add_code_card()
        helpers.wait_load_page(self)
        routes_page.click_add_payment()
        helpers.wait_load_page(self)
        routes_page.click_window_closed_payment()
        helpers.wait_load_page(self)
        number_credit_card = data.card_number
        code_credit_card = data.card_code
        assert routes_page.get_number_card() == number_credit_card
        assert routes_page.get_code_credit_card() == code_credit_card

    # En esta prueba agregamos el mensaje al conductor.
    def test_comment_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        helpers.wait_load_page(self)
        routes_page.add_comment_driver()
        helpers.wait_load_page(self)
        comment_driver = data.message_for_driver
        assert routes_page.get_comment_driver() == comment_driver

    # En esta prueba seleccionamos Manta y pañuelos

    def test_slider_blankets_and_handkerchiefs(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.activate_slider_blankets_and_handkerchiefs()
        helpers.wait_load_page(self)
        assert routes_page.is_switch_checked_blankets_and_handkerchiefs()

    # En esta prueba confirmamos 2 helados y comprobamos que se hayan agregado correctamente
    def test_click_two_ice_cream_value(self):
        routes_page = UrbanRoutesPage(self.driver)
        helpers.wait_load_page(self)
        counter_elements = '2'
        routes_page.add_icecream_amount(counter_elements)
        ice_cream_value = routes_page.get_icecream_counter()
        assert ice_cream_value == counter_elements

    # En esta prueba realizamos el pedido y comprobamos el mensaje final de la página.
    def test_order_taxi_button(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_order_taxi_button()
        time.sleep(60)
        final_message = routes_page.get_message()
        assert "El conductor llegará" in final_message

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

# Prueba