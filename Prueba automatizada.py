import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import data

driver = webdriver.Chrome()  # controlador para usar en este caso Google Chrome
driver.maximize_window()  # Modo de pantalla completa para las pruebas
urban_routes = 'https://cnt-9cef1712-fef7-4933-afd5-2f0f01c456e9.containerhub.tripleten-services.com?lng=es'
driver.get(urban_routes)
current_url = driver.current_url
# assert current_url == 'https://cnt-cb222161-95dc-463b-941e-998082967a4b.containerhub.tripleten-services.com/?lng=es'
driver.implicitly_wait(3)
driver.find_element(By.ID, "from").send_keys(data.address_from)
driver.find_element(By.ID, "to").send_keys(data.address_to)
driver.implicitly_wait(3)
# driver.find_element(By.CSS_SELECTOR, "button.button.round").click()
driver.find_element(By.CLASS_NAME, "button.button.round").click()
time.sleep(5)
driver.quit()