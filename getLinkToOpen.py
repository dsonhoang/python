from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def getLink(driver2, wait2, url, key):
   if url == '':
      return ""

   url = url.strip()

   url = url.replace('(', '').replace(')', '').replace('[', '').replace(']', '')

   if not url.startswith('https://') and not url.startswith('http://'):
      url = 'https://' + url
   try:
      try:
         driver2.get(url)
      except:
         return ""
      # Wait until the page is fully loaded
      wait2.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
      time.sleep(2)
      current_url = driver2.current_url
      if 'google.com/url?q=https://sites.google.com' in current_url:
         next_url = current_url.split('url?q=')[1]
         driver2.get(next_url)
         wait2.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
         time.sleep(1)
         a_tags = driver2.find_elements(By.TAG_NAME, 'a')

         for a in a_tags:
            href = a.get_attribute('href')
            if 'sites' not in href:
               driver2.get(href)
               wait2.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
               time.sleep(1)
               current_url = driver2.current_url
               if 'google.com/search' in current_url:
                  search = driver2.find_element(By.ID, 'search')
                  a_tags = search.find_elements(By.TAG_NAME, 'a')
                  for a in a_tags:
                     href = a.get_attribute('href')
                     if ('google' not in href and 'search' not in href):
                        return href
               else:
                  return current_url

      elif 'sites.google.com' in current_url:
         a_tags = driver2.find_elements(By.TAG_NAME, 'a')

         for a in a_tags:
            href = a.get_attribute('href')
            if 'sites' not in href:
               driver2.get(href)
               wait2.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
               time.sleep(1)
               current_url = driver2.current_url
               if 'google.com/search' in current_url:
                  search = driver2.find_element(By.ID, 'search')
                  a_tags = search.find_elements(By.TAG_NAME, 'a')
                  for a in a_tags:
                     href = a.get_attribute('href')
                     if ('google' not in href and 'search' not in href):
                        return href
               else:
                  return current_url

      elif 'google.com/search' in current_url:
         search = driver2.find_element(By.ID, 'search')
         a_tags = search.find_elements(By.TAG_NAME, 'a')
         for a in a_tags:
            href = a.get_attribute('href')
            if ('google' not in href and 'search' not in href):
               return href

      elif 'medium' in current_url:
         # Find the article element and all a tags within it
         article = driver2.find_elements(By.TAG_NAME, 'article')[0]
         a_tags = article.find_elements(By.TAG_NAME, 'a')

         # Print the href attributes of all a tags within the article
         for a in a_tags:
            href = a.get_attribute('href')
            if 'medium' not in href:
               next_url = href
               driver2.get(next_url)
               wait2.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
               time.sleep(1)
               current_url = driver2.current_url

               if 'pinterest.com' in current_url:
                  time.sleep(3)
                  pin_link = ''
         
                  div_link = driver2.find_elements(By.CSS_SELECTOR, '[data-test-id="visit-button-mobile"]')[0]
                  div_link.click()
                  time.sleep(2)
                  driver2.switch_to.window(driver2.window_handles[-1])
                  url = driver2.current_url
                  driver2.close()
                  driver2.switch_to.window(driver2.window_handles[0])

                  pin_link = url

                  if pin_link != '':
                     driver2.get(pin_link)
                     time.sleep(2)
                     current_url = driver2.current_url
                     if 'google.com/search' in current_url:
                        search = driver2.find_element(By.ID, 'search')
                        a_tags = search.find_elements(By.TAG_NAME, 'a')
                        for a in a_tags:
                           href = a.get_attribute('href')
                           if ('google' not in href and 'search' not in href):
                              return href
                     else:
                        return href

               elif 'google.com/search' in current_url:
                  search = driver2.find_element(By.ID, 'search')
                  a_tags = search.find_elements(By.TAG_NAME, 'a')
                  for a in a_tags:
                     href = a.get_attribute('href')
                     if ('google' not in href and 'search' not in href):
                        return href
               elif 'twitter.com' in current_url:
                  time.sleep(5)
                  article = driver2.find_element(By.TAG_NAME, 'body')
                  a_tags = article.find_elements(By.TAG_NAME, 'a')
                  for a in a_tags:
                     href = a.get_attribute('href')
                     if 'twitter.com' not in href:
                        driver2.get(href)
                        wait2.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                        time.sleep(1)
                        current_url = driver2.current_url
                        if 'google.com/search' in current_url:
                           search = driver2.find_element(By.ID, 'search')
                           a_tags = search.find_elements(By.TAG_NAME, 'a')
                           for a in a_tags:
                              href = a.get_attribute('href')
                              if ('google' not in href and 'search' not in href):
                                 return href
                        else:
                           return current_url

      elif 'pinterest.com' in current_url:
         time.sleep(3)
         pin_link = ''
         
         div_link = driver2.find_elements(By.CSS_SELECTOR, '[data-test-id="visit-button-mobile"]')[0]
         div_link.click()
         time.sleep(2)
         driver2.switch_to.window(driver2.window_handles[-1])
         url = driver2.current_url
         driver2.close()
         driver2.switch_to.window(driver2.window_handles[0])

         pin_link = url

         if pin_link != '':
            driver2.get(pin_link)
            time.sleep(2)
            current_url = driver2.current_url
            if 'google.com/search' in current_url:
               search = driver2.find_element(By.ID, 'search')
               a_tags = search.find_elements(By.TAG_NAME, 'a')
               for a in a_tags:
                  href = a.get_attribute('href')
                  if ('google' not in href and 'search' not in href):
                     return href
            else:
               return href

      elif 'twitter.com' in current_url:
         time.sleep(5)
         article = driver2.find_element(By.TAG_NAME, 'body')
         a_tags = article.find_elements(By.TAG_NAME, 'a')
         for a in a_tags:
            href = a.get_attribute('href')
            if 'twitter.com' not in href:
               driver2.get(href)
               wait2.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
               time.sleep(2)
               current_url = driver2.current_url
               if 'google.com/search' in current_url:
                  search = driver2.find_element(By.ID, 'search')
                  a_tags = search.find_elements(By.TAG_NAME, 'a')
                  for a in a_tags:
                     href = a.get_attribute('href')
                     if ('google' not in href and 'search' not in href):
                        return href
               else:
                  return current_url
      return ""
   except Exception as e:
      if key == 'admin':
         print('Exception at getLink', e)
         import traceback
         traceback.print_exc()
      return ""