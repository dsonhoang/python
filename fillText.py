from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import numpy as np
from . import func
from . import getPost
import urllib.parse

from urllib.parse import urlparse

def get_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith("www."):
        domain = domain[4:]  # Remove the "www." prefix
    return domain

def extract_text_between_quotes(input_string):
    first_quote_index = input_string.find('"')
    if first_quote_index != -1:
        second_quote_index = input_string.find('"', first_quote_index + 1)
        if second_quote_index != -1:
            extracted_text = input_string[first_quote_index + 1:second_quote_index]
            return extracted_text
    return None

def send(driver, count, text_value):
   if text_value == '':
      return
   try_count = 0
   while True:
      time.sleep(0.5)
      text_area = None
      try:
         text_area = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'proof_' + str(count))))
      except:
         text_area = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'vproof')))

      if text_area is not None:
         if text_area.get_attribute('value') is not None and text_area.get_attribute('value') != '':
            break
      driver.execute_script("arguments[0].value = arguments[1];", text_area, text_value)

      try_count += 1
      if try_count == 3:
         break

#def fill(lkey, driver, driver2, post_urls, last_paragraps, post_articles, requirements, phan_loai, ads_infor, dich_den, link_to_open, code, link_code):
def fill(driver, driver2, phan_loai, requirements, sorted_url, post_urls, post_articles, ads_infor, link_to_open, code, link_code, lkey):
   count = 1
   try:
      for requirement in requirements:
         if func.typeOfRequirement(requirement, phan_loai) == 0:
            index = phan_loai[requirement][1]
            if index == -99:
               #-> send random
               random_url = random.choice(post_urls)
               send(driver, count, random_url)
            elif index == -1:
               #-> send last sorted url
               send(driver, count, sorted_url[-1])
            else:
               #-> send [index - 1]
               if index > 0 and index < len(sorted_url):
                  send(driver, count, sorted_url[index - 1])
               elif index > 0 and index > len(sorted_url) and index < len(post_urls):
                  send(driver, count, post_urls[index - 1])
               else:
                  random_url = random.choice(sorted_url)
                  send(driver, count, random_url)

         elif func.typeOfRequirement(requirement, phan_loai) == 0.2:
            #-> send two random url
            random_url1 = random.choice(sorted_url)
            random_url2 = random.choice(sorted_url)

            while random_url2 == random_url1:
               random_url2 = random.choice(sorted_url)

            send(driver, count, random_url1 + "\n" + random_url2)

         elif func.typeOfRequirement(requirement, phan_loai) == 0.9:
            re_domain = ''
            if 'hint:' in requirement:
               re_domain = requirement.split('hint:')[1].strip()
            elif 'hint :' in requirement:
               re_domain = requirement.split('hint :')[1].strip()
            elif 'hint' in requirement:
               re_domain = requirement.split('hint')[1].strip()

            find_domain = get_domain(random.choice(post_urls))

            if re_domain.endswith('d*'):
               find_domain = find_domain.replace('id', 'id/')
            if 'www.' in re_domain:
               find_domain = 'www.' + find_domain
            if 'https://' in re_domain:
               find_domain = 'https://' + find_domain
            if '/**/' in re_domain or '/en/' in re_domain or '/*n/' in re_domain:
               find_domain = find_domain + '/en/'

            if re_domain[-1] == '/' and find_domain[-1] != '/':
               find_domain = find_domain + '/'

            matched = True

            if abs(len(re_domain) - len(find_domain)) > 5:
               matched = False
            if re_domain[0] != '*' and re_domain[0] != find_domain[0]:
               matched = False
            if re_domain.count('/') != find_domain.count('/'):
               matched = False

            if matched:
               send(driver, count, find_domain)
            #-> send domain
         #-------------------------------------------------------------------------------------

         elif func.typeOfRequirement(requirement, phan_loai) == 1:
            url_index = phan_loai[requirement][1]
            paragrap_index = phan_loai[requirement][2]
            sorted_para = []

            #-> go to post url_index -> send para paragrap_index
            if url_index == -99:
               #-> send random
               sorted_para = getPost.get_sorted_para(driver2, random.choice(sorted_url), lkey)
            elif url_index == -1:
               sorted_para = getPost.get_sorted_para(driver2, sorted_url[-1], lkey)
            else:
               #-> send [index - 1]
               if url_index > 0 and url_index <= len(sorted_url):
                  sorted_para = getPost.get_sorted_para(driver2, sorted_url[url_index - 1], lkey)
               elif url_index > 0 and url_index > len(sorted_url) and url_index <= len(post_urls):
                  sorted_para = getPost.get_sorted_para(driver2, post_urls[url_index - 1], lkey)
               else:
                  sorted_para = getPost.get_sorted_para(driver2, random.choice(post_urls), lkey)

            if len(sorted_para) > 0:
               if paragrap_index == -99:
                  send(driver, count, random.choice(sorted_para))
               elif paragrap_index == -1:
                  send(driver, count, sorted_para[-1])
               else:
                  if paragrap_index > 0 and paragrap_index < len(sorted_para):
                     send(driver, count, sorted_para[paragrap_index - 1])
                  else:
                     send(driver, count, random.choice(sorted_para))

         elif func.typeOfRequirement(requirement, phan_loai) == 1.9:
            article_name = extract_text_between_quotes(requirement)
            if article_name is not None:
               try:
                  driver2.get('https://' + get_domain(post_urls[0]) + '/?s=' + urllib.parse.quote(article_name).replace('%20', '+'))
                  time.sleep(2)

                  a_tags = driver2.find_elements(By.TAG_NAME, 'a')

                  for i in range(len(a_tags)):
                     if a_tags[i] is not None:
                        if a_tags[i].text.lower() == article_name.lower():
                           sorted_para = getPost.get_sorted_para(driver2, a_tags[i].get_attribute('href'), lkey)
                           send(driver, count, sorted_para[-1])
                           break
               except:
                  pass

         #-------------------------------------------------------------------------------------
         elif func.typeOfRequirement(requirement, phan_loai) == 2:
            url_index = phan_loai[requirement][1]
            sen_index = phan_loai[requirement][2]
            sorted_para = []

            if url_index == -99:
               #-> send random
               sorted_para = getPost.get_sorted_para(driver2, random.choice(sorted_url), lkey)
            elif url_index == -1:
               sorted_para = getPost.get_sorted_para(driver2, sorted_url[-1], lkey)
            else:
               #-> send [index - 1]
               if url_index > 0 and url_index < len(sorted_url):
                  sorted_para = getPost.get_sorted_para(driver2, sorted_url[url_index - 1], lkey)
               elif url_index > 0 and url_index > len(sorted_url) and url_index < len(post_urls):
                  sorted_para = getPost.get_sorted_para(driver2, post_urls[url_index - 1], lkey)
               else:
                  sorted_para = getPost.get_sorted_para(driver2, random.choice(post_urls), lkey)
                  #'https://sproutgigs.com/jobs/submit-task.php?Id=9ed3d380958b59470ea3e2a7'

            if len(sorted_para) > 0:
               if sen_index == -1:
                  for sentence in sorted_para[::-1]:
                     if '.' not in sentence:
                        send(driver, count, sentence + ".")
                        break
                     else:
                        arr = sentence.split('.')
                        for e in arr[::-1]:
                           e = e.strip()
                           if len(e) > 20:
                              send(driver, count, e + ".")
                              break

         elif func.typeOfRequirement(requirement, phan_loai) == 2.1:
            sorted_para = getPost.get_sorted_para(driver2, random.choice(sorted_url), lkey)
            if len(sorted_para) > 0:
               word = sorted_para[-1].split(' ')[-1]
               if word[-1] != '.':
                  word += '.'

               send(driver, count, word)
         #-------------------------------------------------------------------------------------

         elif func.typeOfRequirement(requirement, phan_loai) == 3:
            send(driver, count, ads_infor["main"])

         elif func.typeOfRequirement(requirement, phan_loai) == 3.1:
            send(driver, count, ads_infor["about"].split("|")[0])

         elif func.typeOfRequirement(requirement, phan_loai) == 3.2:
            send(driver, count, ads_infor["contact"].split("|")[0])

         elif func.typeOfRequirement(requirement, phan_loai) == 3.3:
            if "|1" in ads_infor["about"]:
               send(driver, count, ads_infor["main"] + "\n" + ads_infor["about"].split("|")[0])
            elif "|1" in ads_infor["contact"]:
               send(driver, count, ads_infor["main"] + "\n" + ads_infor["contact"].split("|")[0])
            else:
               send(driver, count, ads_infor["main"] + "\n" + ads_infor["inside1"])

         elif func.typeOfRequirement(requirement, phan_loai) == 3.5:
            if ads_infor["para1"] != '':
               send(driver, count, ads_infor["para1"])
               ads_infor["para1"] = ''
            elif ads_infor["para2"] != '':
               send(driver, count, ads_infor["para2"])
               ads_infor["para2"] = ''

         elif func.typeOfRequirement(requirement, phan_loai) == 3.6:
            send(driver, count, ads_infor["inside1"] + "\n" + ads_infor["inside2"])

         #-------------------------------------------------------------------------------------

         #ID
         elif func.typeOfRequirement(requirement, phan_loai) == 9:
            driver2.get(link_to_open)
            time.sleep(1)

            # Switch to the new tab
            ID = driver2.find_elements(By.CLASS_NAME, 'code-block')
            for id in ID:
               if id.text.startswith("ID") or id.text.startswith("Id") or id.text.startswith("id"):
                  id_code = id.text
                  break

            send(driver, count, id_code)

         elif func.typeOfRequirement(requirement, phan_loai) == 99:
            if code is not None and code != '':
               send(driver, count, code)

         elif func.typeOfRequirement(requirement, phan_loai) == 50:
            if link_code is not None and link_code != '':
               send(driver, count, link_code)

         count += 1
         time.sleep(1)
   except Exception as e:
      if lkey == 'admin':
         print('Exception at fill text', e)
         import traceback
         traceback.print_exc()