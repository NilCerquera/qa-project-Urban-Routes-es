from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import data
driver = webdriver.Chrome()  # controlador para usar en este caso Google Chrome
driver.maximize_window()  # Modo de pantalla completa para las pruebas
driver.get(data.urban_routes_url)
current_url = driver.current_url
driver.implicitly_wait(3)
driver.find_element(By.ID, "from").send_keys(data.address_from)
driver.find_element(By.ID, "to").send_keys(data.address_to)
driver.implicitly_wait(3)
# driver.find_element(By.CSS_SELECTOR, "button.button.round").click()
driver.find_element(By.CLASS_NAME, "button.button.round").click()
driver.implicitly_wait(3)
element_comfort = driver.find_element(By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")
element_comfort.click()
driver.implicitly_wait(3)
driver.find_element(By.CSS_SELECTOR, "div.np-button").click()
driver.implicitly_wait(3)
driver.find_element(By.ID, "phone").send_keys(data.phone_number)
driver.find_element(By.CLASS_NAME, "button.button.full").click()

time.sleep(3)
driver.quit()