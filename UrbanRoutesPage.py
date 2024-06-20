from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import data

# Corrección 2, creamos el archivo UrbanRoutesPage para agregar los controladores y funciones


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
    confirmed_phone = (By.XPATH, ".//div[@class='np-text']")
    button_payment = (By.CSS_SELECTOR, ".pp-button")
    add_credit_Card = (By.CSS_SELECTOR, ".pp-row.disabled")
    number_credit_card = (By.ID, "number")
    code_credit_card = (By.XPATH, ".//div[@class='card-code-input']/input[@id='code']")
    click_payment = (By.XPATH, ".//div[@class='pp-buttons']//button[text()='Agregar']")
    card_added = (By.ID, 'card-1')
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

    # Seleccionamos el boton continuar
    def select_continue(self):
        self.driver.find_element(*self.select_number).click()

    # Traemos el codigo SMS para el telefono y poder guardar el número telefonico
    def send_code(self, code):
        self.driver.find_element(*self.code_phone).send_keys(code)

    # Hacemos click en el botón para guardar el número de telefono
    def ok_code(self):
        self.driver.find_element(*self.submit_code).click()

    # Obtener el número telefónico
    def get_number_phone(self):
        number_completed = self.driver.find_element(*self.confirmed_phone).text  # Seleccionamos la opción continuar
        return number_completed

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

    # Agregamos el número de código
    def add_code_card(self):
        self.driver.find_element(*self.code_credit_card).send_keys(data.card_code)
        self.driver.find_element(*self.code_credit_card).send_keys(Keys.TAB)

# Realizamos un click para agregar el metodo de pago
    def click_add_payment(self):
        self.driver.find_element(*self.click_payment).click()

# Obtenemos si la tarjeta se agregó correctamente
    def get_card_id(self):
        return self.driver.find_element(*self.card_added)

#   Confirmamos si esta seleccionado la tarjeta
    def is_card_1_checked(self) -> object:
        card_checkbox = self.driver.find_element(*self.card_added)
        return card_checkbox.is_selected()
    # Hacemos click para cerrar la pagina

# Cerramos la ventana de metódo de pago
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
