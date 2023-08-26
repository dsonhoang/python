from urllib.parse import urlparse
from datetime import datetime
import random
import string
from bs4 import BeautifulSoup

def get_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith("www."):
        domain = domain[4:]  # Remove the "www." prefix
    return domain

def writeLog(index, number):
   f = open("log.txt", "a")
   time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
   f.write(f"\n{time} Profile{index}: {number}")
   f.close()

def change_requirements(requirements, phan_loai):
   for i in range(len(requirements)):
      if requirements[i] not in phan_loai.keys():
         for key in phan_loai.keys():
            if requirements[i] in key or key in requirements[i]:
               if phan_loai[key][0] != 0.9 and phan_loai[key][0] != 1.9:
                  requirements[i] = key
                  break

def typeOfRequirement(requirement, phan_loai):
   for key in phan_loai.keys():
      if requirement == key:
         return phan_loai[key][0]

   for key in phan_loai.keys():
      if requirement in key or key in requirement:
         return phan_loai[key][0]
   
   return -1

def writeLink(link, key):
   if key != "admin":
      return
   exits = False
   with open('du_lieu1.txt', 'r+', encoding='utf-8') as file:
      urls = file.readlines()
      for url in urls:
         if link in url:
            exits = True
            break

      if not exits:
         file.write(link + '\n')
   file.close()

def writeRequirement(requirement, key):
   if key != 'admin':
      return
   exits = False
   with open('du_lieu2.txt', 'r+', encoding='utf-8') as file:
      requirements = file.readlines()
      for e in requirements:
         if requirement in e:
            exits = True
            break

      if exits == False:
         file.write(requirement + '\n')
   file.close()

def writeAds(ads_main):
   exits = False
   with open('ads.txt', 'r+', encoding='utf-8') as file:
      urls = file.readlines()
      if len(urls) > 20:
         urls = urls[-20:]
      for url in urls:
         if get_domain(ads_main) in url:
            exits = True
            break

      if not exits:
         file.write(ads_main + '\n')
   file.close()

def change_gclid(gmain):
   gclid = get_gclid(gmain)
   first = generate_random_string(7)
   new_gclid = gclid.replace(gclid[12: 12 + 7], first)
   return gmain.replace(gclid, new_gclid)

def generate_random_string(length):
   characters = string.ascii_letters + string.digits
   random_string = ''.join(random.choice(characters) for _ in range(length))

   while 'ad' in random_string.lower():
      random_string = ''.join(random.choice(characters) for _ in range(length))
   return random_string

def get_random_ads(recent_ads):
   with open('ads.txt', "r") as file:
      ads_list = file.read().splitlines()

   if len(ads_list) > 20:
      ads_list = ads_list[-20:]
   while True:
      ads = random.choice(ads_list)
      if get_domain(ads) not in recent_ads:
         return change_gclid(ads)

   return ""

def get_gclid(string):
   start_index = string.find('gclid=') + len('gclid=')
   end_index = string.find('BwE', start_index)
    
   if start_index >= len('gclid') and end_index != -1:
      extracted_text = string[start_index:end_index + len('BwE')]
      return extracted_text
   else:
      return None

def getFirstUrl(details):
   black_words = ['jpg', 'png', 'prnt', 'ibb', '*', 'img', 'paste', 'snip', 'window', 'blocked', 'instruction', '..']
   lines = details.split('\n')

   for line in lines:
      words = line.split(' ')
      for word in words:
         word = word.strip()
         if word.lower() == 'google.com':
            continue
         flag = False
         if '.' in word and word.find('.') != len(word)-1:
            for i in black_words:
               if i in word:
                  flag = True
                  break
            if not flag and 'red arrow' not in line:
               return word

   return ''