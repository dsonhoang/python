from selenium import webdriver
from selenium.webdriver.common.by import By

def find(driver2, link_to_open):
  driver2.get(link_to_open)
  text_value = ''
  try:
    text_value = driver2.find_element(By.ID, 'kode').text
  except:
    pass
  return text_value
