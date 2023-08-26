from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import urlparse

def matched_url(current_url, herf_url):
   black_words = ['home', 'resource', 'sitemap', 'tentang-kami', 
   'upload','pasang', 'category', 'author', 'page', 'disclaimer', 
   'privacy', 'policy', 'about', 'contac', 'tag', 'cookies', 'search', 
   'topic', 'topik', 'politica', 'legal', 'term', 'login', 'content', 'page']
   if current_url == herf_url:
      return False
   domain1 = urlparse(current_url).netloc

   domain2 = urlparse(herf_url).netloc

   if domain1 != domain2 or len(herf_url) - 20 < len(domain1):
      return False
   if any(word in herf_url for word in black_words):
      return False
   else:
      return True

def get_sorted_url(driver2, url, lkey):
   try:
      try:
         driver2.get(url)
      except:
         return []
      time.sleep(2)
      if driver2.find_elements(By.CLASS_NAME, 'inside-right-sidebar'):
         block_3_element = driver2.find_element(By.CLASS_NAME, 'inside-right-sidebar')

         a_tags = block_3_element.find_elements(By.TAG_NAME, 'a')
         if a_tags is not None and len(a_tags) > 0:
            for i in range(len(a_tags)):
               if a_tags[i] is not None:
                  a_tags[i] = a_tags[i].get_attribute('href')

         return a_tags
      else:
         return []
   except Exception as e:
      if lkey == 'admin':
         print("Exception at get_sorted_url", e)
         import traceback
         traceback.print_exc()
      return []

def get_sorted_para(driver2, url, lkey):
   try:
      paragraps = []
      count = 0
      while len(paragraps) == 0 and count < 3:
         try:
            driver2.get(url)
         except:
            pass
         time.sleep(2)

         if driver2.find_elements(By.CLASS_NAME, 'entry-content'):
            entry_content = driver2.find_element(By.CLASS_NAME, 'entry-content')

            p_elements = entry_content.find_elements(By.TAG_NAME, 'p')
            li_elements = entry_content.find_elements(By.TAG_NAME, 'li')

         else:
            p_elements = driver2.find_elements(By.TAG_NAME, 'p')
            li_elements = driver2.find_elements(By.TAG_NAME, 'li')

         all_elements = p_elements + li_elements
         all_elements = sorted(all_elements, key=lambda element: (element.location['y']))

         for element in all_elements:
            if element.find_elements(By.TAG_NAME, 'a') and len(element.text) < 200:
               continue
            elif len(element.text) > 50:
               paragraps.append(element.text.strip())

         count += 1

      if len(paragraps) < 5:
         return []
         
      tmp = []
      for i in range(len(paragraps) - 1):
         if len(paragraps[i]) >= 150:
            tmp.append(paragraps[i])
         else:
            tmp.append(paragraps[i] + "\n" + paragraps[i + 1])
            i += 1

      if len(paragraps[-1]) > 150:
         tmp.append(paragraps[-1])
      else:
         tmp.append(paragraps[len(paragraps) - 2] + "\n" + paragraps[-1])

      return tmp
   except Exception as e:
      if lkey == 'admin':
         print('Exception at get_sorted_para', e)
         import traceback
         traceback.print_exc()
      return []

def get_all_url(driver2, url, post_urls, post_articles, lkey):
   try:
      try:
         driver2.get(url)
      except:
         return
      time.sleep(2)
      a_tags = driver2.find_elements(By.TAG_NAME, 'a')

      for a in a_tags:
         if a is None:
            continue
         try:
            a_href = a.get_attribute('href').split('#')[0]
            a_href = a_href.split('?')[0]
            if matched_url(url, a_href) and a_href not in post_urls:
               post_urls.append(a_href)

               a_text = a.text.strip()
               tmp = a_text + "|" + a_href
               if tmp not in post_articles:
                  post_articles.append(tmp)
         except:
            pass

   except Exception as e:
      if lkey == 'admin':
         print('Exception at get_all_url', e)
         import traceback
         traceback.print_exc()
      pass