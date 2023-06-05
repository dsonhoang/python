from selenium import webdriver
from selenium.webdriver.common.by import By

def find(driver2, link_to_open):
  try:
    driver2.get(link_to_open)
    text_value = ''
    try:
      text_value = driver2.find_element(By.ID, 'kode').text
    except:
      pass
    if text_value == '':
      print('Khong tim thay code')
    else:
      print(text_value)
    return text_value
  except:
    return ''
