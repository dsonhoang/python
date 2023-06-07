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
      a_tags = driver2.find_elements(By.TAG_NAME, 'a')
      if a_tags is not None::
          for a_tag in a_tags[::-1]:
            if a_tag is not None:
              try:
                driver2.get(a_tag.get_attribute('href'))
                p_tags = driver2.find_elements(By.TAG_NAME, 'p')
                for p in p_tags:
                  if p is not None:
                    if 'CODE:' in p.text:
                      text_value = p.text
                      print(text_value)
                      return text_value
              except:
                pass
    else:
      print(text_value)
    return text_value
  except:
    return ''
